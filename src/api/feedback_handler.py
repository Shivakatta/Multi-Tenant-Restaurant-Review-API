"""
Feedback Handler - Core API Business Logic

Orchestrates feedback submission, tenant resolution, and insights generation.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.external.sentiment_service import SentimentService
from src.models.feedback import Feedback
from src.models.tenant import Tenant
from src.storage.dynamodb_client import DynamoDBClient
from src.storage.s3_client import S3Client
from src.utils.cache import cache
from src.utils.exceptions import (
    InvalidAPIKeyException,
    RateLimitException,
    TenantNotFoundException,
    ValidationException,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FeedbackHandler:
    """Main handler for feedback operations with multi-tenant support."""

    def __init__(
        self,
        db_client: DynamoDBClient,
        s3_client: S3Client,
        sentiment_service: SentimentService,
    ) -> None:
        """
        Initialize handler with dependencies.

        Args:
            db_client: DynamoDB client (or mock)
            s3_client: S3 client (or mock)
            sentiment_service: Sentiment analysis service
        """
        self.db_client = db_client
        self.s3_client = s3_client
        self.sentiment_service = sentiment_service
        self._tenant_cache: dict[str, Tenant] = {}

    def _get_registry_path(self) -> Path:
        return Path(__file__).resolve().parents[2] / "config" / "tenant_registry.json"

    def _load_tenant_registry(self) -> dict[str, object]:
        registry = self.s3_client.download_json("tenants/tenant_registry.json")
        if registry is not None:
            return registry

        registry_path = self._get_registry_path()
        try:
            with registry_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError as exc:
            logger.error("tenant_registry.json not found", extra={"path": str(registry_path)})
            raise TenantNotFoundException("Tenant registry not found") from exc
        except json.JSONDecodeError as exc:
            logger.error("tenant_registry.json invalid", extra={"path": str(registry_path)})
            raise TenantNotFoundException("Tenant registry invalid") from exc

    @cache(ttl_seconds=60)
    def load_tenant_by_api_key(self, api_key: str) -> Tenant:
        """
        Resolve tenant from API key with caching.

        Args:
            api_key: Restaurant API key from request header

        Returns:
            Tenant object or None if not found
        """
        if not api_key or not isinstance(api_key, str):
            raise InvalidAPIKeyException("API key must be a non-empty string")

        registry = self._load_tenant_registry()
        tenants = registry.get("tenants", [])

        for raw_tenant in tenants:
            if raw_tenant.get("api_key") == api_key:
                return Tenant.from_dict(raw_tenant)

        raise TenantNotFoundException("Tenant not found for provided API key")

    def submit_feedback(
        self,
        api_key: str,
        customer_name: str,
        rating: int,
        comment: str,
    ) -> dict[str, object]:
        """Submit customer feedback."""
        logger.info(
            "Feedback submission started",
            extra={"customer": customer_name, "rating": rating},
        )
        
        try:
            if not api_key or not isinstance(api_key, str):
                raise InvalidAPIKeyException("API key is required")
        except InvalidAPIKeyException as e:
            logger.error(f"Authentication failed: {str(e)}", extra={"error_type": "auth"})
            raise

        try:
            tenant = self.load_tenant_by_api_key(api_key)
        except TenantNotFoundException as e:
            logger.error(f"Tenant not found: {str(e)}", extra={"error_type": "tenant"})
            raise

        try:
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValidationException("rating must be an integer between 1 and 5")

            if not comment or not comment.strip():
                raise ValidationException("comment must not be empty")
        except ValidationException as e:
            logger.error(f"Validation failed: {str(e)}", extra={"error_type": "validation"})
            raise

        sentiment = None
        if tenant.sentiment_analysis:
            try:
                sentiment_result = self.sentiment_service.analyze_sentiment(comment)
                sentiment = {
                    "score": sentiment_result["score"],
                    "label": sentiment_result["label"],
                }
            except Exception as exc:
                logger.warning(
                    "Sentiment analysis failed, continuing without sentiment",
                    extra={"tenant_id": tenant.tenant_id, "error": str(exc)},
                )
                sentiment = None

        try:
            daily_count = self.db_client.get_daily_submission_count(tenant.tenant_id)
            if daily_count >= 100:
                logger.warning(
                    "Rate limit exceeded",
                    extra={"tenant_id": tenant.tenant_id, "daily_submissions": daily_count},
                )
                raise RateLimitException("Daily feedback submission limit exceeded")
        except RateLimitException as e:
            logger.error(f"Rate limit error: {str(e)}", extra={"error_type": "rate_limit"})
            raise

        feedback = Feedback(
            tenant_id=tenant.tenant_id,
            customer_name=customer_name or None,
            rating=rating,
            comment=comment,
            sentiment_score=sentiment["score"] if sentiment else None,
            sentiment_label=sentiment["label"] if sentiment else None,
        )

        self.db_client.save_feedback(tenant.tenant_id, feedback.to_dict())
        self.db_client.increment_daily_submission_count(tenant.tenant_id)
        logger.info(
            "Feedback submitted",
            extra={"tenant_id": tenant.tenant_id, "feedback_id": feedback.feedback_id},
        )

        return {
            "feedback_id": feedback.feedback_id,
            "tenant_id": tenant.tenant_id,
            "rating": feedback.rating,
            "sentiment": sentiment,
            "created_at": feedback.created_at,
            "message": "Thank you for your feedback!",
        }

    def get_restaurant_insights(self, api_key: str) -> dict[str, object]:
        """Get insights for a restaurant."""
        if not api_key or not isinstance(api_key, str):
            raise InvalidAPIKeyException("API key is required")

        tenant = self.load_tenant_by_api_key(api_key)
        feedback_items = self.db_client.list_feedback(tenant.tenant_id, limit=1000)

        total_feedback = len(feedback_items)
        average_rating = (
            round(sum(item["rating"] for item in feedback_items) / total_feedback, 2)
            if total_feedback
            else 0.0
        )

        rating_distribution = {str(value): 0 for value in range(1, 6)}
        for item in feedback_items:
            rating_distribution[str(item.get("rating", 0))] += 1

        sentiment_summary = None
        if tenant.sentiment_analysis and feedback_items:
            sentiment_scores = [
                item["sentiment_score"]
                for item in feedback_items
                if item.get("sentiment_score") is not None
            ]
            if sentiment_scores:
                sentiment_summary = {
                    "average_score": round(sum(sentiment_scores) / len(sentiment_scores), 2),
                    "positive_count": sum(
                        1 for item in feedback_items if item.get("sentiment_label") == "positive"
                    ),
                    "neutral_count": sum(
                        1 for item in feedback_items if item.get("sentiment_label") == "neutral"
                    ),
                    "negative_count": sum(
                        1 for item in feedback_items if item.get("sentiment_label") == "negative"
                    ),
                }

        recent_feedback = feedback_items[:5]

        logger.info(
            "Restaurant insights generated",
            extra={"tenant_id": tenant.tenant_id, "total_feedback": total_feedback},
        )

        return {
            "tenant_id": tenant.tenant_id,
            "total_feedback": total_feedback,
            "average_rating": average_rating,
            "rating_distribution": rating_distribution,
            "sentiment_summary": sentiment_summary,
            "recent_feedback": recent_feedback,
        }
