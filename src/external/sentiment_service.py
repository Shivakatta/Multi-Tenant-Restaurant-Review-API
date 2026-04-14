"""
Sentiment Analysis Service

Mock implementation of external sentiment analysis API using keyword matching.
"""

import random
from typing import Dict


class SentimentService:
    """Mock sentiment analysis service with keyword-based scoring."""

    def __init__(self, api_key: str = None):
        """
        Initialize sentiment service.

        Args:
            api_key: API key for authentication (not used in mock)
        """
        self.api_key = api_key
        self.positive_words = [
            "great", "excellent", "amazing", "love", "best", 
            "wonderful", "delicious", "fantastic", "perfect", "awesome"
        ]
        self.negative_words = [
            "bad", "terrible", "awful", "hate", "worst", 
            "disgusting", "never", "poor", "horrible", "disappointing"
        ]

    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text using keyword matching.

        Args:
            text: Text to analyze

        Returns:
            {
                "score": float,      # -1.0 to 1.0
                "label": str,        # "positive", "neutral", "negative"
                "confidence": float  # 0.0 to 1.0
            }

        Raises:
            ValueError: If text is empty
            Exception: Simulates 1% API failure rate
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Simulate 1% API failure rate
        if random.random() < 0.01:
            raise Exception("Sentiment API temporarily unavailable")

        text_lower = text.lower()

        # Count positive/negative words
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)

        # Calculate score
        if positive_count > negative_count:
            score = min(0.9, 0.3 + (positive_count * 0.2))
            label = "positive"
        elif negative_count > positive_count:
            score = max(-0.9, -0.3 - (negative_count * 0.2))
            label = "negative"
        else:
            score = 0.0
            label = "neutral"

        return {
            "score": round(score, 2),
            "label": label,
            "confidence": 0.85
        }
