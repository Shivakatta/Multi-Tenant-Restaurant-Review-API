"""
S3 Mock Client for Tenant Configuration Storage

Provides in-memory storage simulation for S3 with JSON support.
"""

import json
from typing import Optional, Dict, List


class S3Client:
    """In-memory S3 client for configuration storage."""

    def __init__(self):
        """Initialize in-memory storage: {s3_key: file_content}"""
        self._storage: Dict[str, str] = {}

    def upload_json(self, key: str, data: dict) -> None:
        """
        Upload JSON data to S3 key.

        Args:
            key: S3 key path (e.g., "tenants/pizza-palace/config.json")
            data: Dict to serialize as JSON
        """
        try:
            self._storage[key] = json.dumps(data)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to serialize JSON: {str(e)}")

    def download_json(self, key: str) -> Optional[Dict]:
        """
        Download and parse JSON from S3.

        Returns:
            Dict or None if key doesn't exist
        """
        if key not in self._storage:
            return None

        try:
            return json.loads(self._storage[key])
        except (json.JSONDecodeError, TypeError) as e:
            return None

    def list_keys(self, prefix: str) -> List[str]:
        """
        List all keys starting with prefix.

        Args:
            prefix: S3 key prefix (e.g., "tenants/")

        Returns:
            List of matching keys
        """
        return [key for key in self._storage.keys() if key.startswith(prefix)]
