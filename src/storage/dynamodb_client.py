"""
DynamoDB Mock Client for Multi-Tenant Feedback Storage

Provides in-memory storage simulation for DynamoDB with complete tenant isolation.
"""

from typing import Optional, Dict, List


class DynamoDBClient:
    """In-memory DynamoDB client with tenant isolation support."""

    def __init__(self):
        """Initialize in-memory storage: {tenant_id: [feedback_items]}"""
        self._storage: Dict[str, List[Dict]] = {}
        self._daily_counts: Dict[str, int] = {}

    def save_feedback(self, tenant_id: str, feedback: dict) -> None:
        """
        Save feedback to tenant-specific table.

        Args:
            tenant_id: Restaurant identifier
            feedback: Feedback dict (from feedback.to_dict())

        Raises:
            ValueError: If tenant_id is empty
        """
        if not tenant_id or not isinstance(tenant_id, str):
            raise ValueError("tenant_id must be a non-empty string")

        if tenant_id not in self._storage:
            self._storage[tenant_id] = []

        self._storage[tenant_id].append(feedback)

    def get_feedback_by_id(self, tenant_id: str, feedback_id: str) -> Optional[Dict]:
        """
        Retrieve a specific feedback item.

        Returns:
            Feedback dict or None if not found
        """
        if tenant_id not in self._storage:
            return None

        for item in self._storage[tenant_id]:
            if item.get("feedback_id") == feedback_id:
                return item

        return None

    def list_feedback(self, tenant_id: str, limit: int = 100) -> List[Dict]:
        """
        Get all feedback for a tenant (most recent first).

        Args:
            tenant_id: Restaurant identifier
            limit: Max number of items to return

        Returns:
            List of feedback dicts, sorted by created_at descending
        """
        if tenant_id not in self._storage:
            return []

        items = sorted(
            self._storage[tenant_id],
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )
        return items[:limit]

    def get_feedback_count(self, tenant_id: str) -> int:
        """Count total feedback items for tenant."""
        if tenant_id not in self._storage:
            return 0
        return len(self._storage[tenant_id])

    def delete_all_feedback(self, tenant_id: str) -> int:
        """
        Delete all feedback for tenant (for testing).

        Returns:
            Number of items deleted
        """
        if tenant_id not in self._storage:
            return 0

        count = len(self._storage[tenant_id])
        del self._storage[tenant_id]
        return count

    def get_daily_submission_count(self, tenant_id: str) -> int:
        """Get daily submission count for tenant."""
        return self._daily_counts.get(tenant_id, 0)

    def increment_daily_submission_count(self, tenant_id: str) -> int:
        """Increment daily submission count and return new count."""
        self._daily_counts[tenant_id] = self._daily_counts.get(tenant_id, 0) + 1
        return self._daily_counts[tenant_id]

    def reset_daily_counts(self) -> None:
        """Reset all daily submission counts."""
        self._daily_counts.clear()
