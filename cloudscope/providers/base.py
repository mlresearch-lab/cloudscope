"""Base provider interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseProvider(ABC):
    """Abstract base class for cloud providers."""

    def __init__(self, credentials: Dict[str, str], region: str = "us-east-1"):
        self.credentials = credentials
        self.region = region

    @abstractmethod
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all resources in the account."""
        ...

    @abstractmethod
    async def get_metrics(self, resource_id: str) -> Dict[str, Any]:
        """Get metrics for a specific resource."""
        ...

    @abstractmethod
    async def get_cost_data(self, start_date: str, end_date: str) -> Dict[str, float]:
        """Get cost data for a date range."""
        ...
