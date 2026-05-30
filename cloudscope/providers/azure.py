"""Azure Monitor integration."""

from .base import BaseProvider


class AzureProvider(BaseProvider):
    """Azure resource monitoring via Monitor API."""

    def __init__(self, credentials: dict, region: str = "eastus"):
        super().__init__(credentials, region)
        self.subscription_id = credentials.get("subscription_id")

    async def list_resources(self):
        return []

    async def get_metrics(self, resource_id: str):
        return {"cpu": 0, "memory": 0, "net_in": 0, "net_out": 0}

    async def get_cost_data(self, start_date, end_date):
        return {}
