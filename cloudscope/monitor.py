"""Core monitoring module for multi-cloud resources."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ResourceMetrics:
    """Metrics snapshot for a cloud resource."""
    resource_id: str
    provider: str
    region: str
    cpu_utilization: float
    memory_utilization: float
    network_in_bytes: int
    network_out_bytes: int
    cost_per_hour: float
    uptime_hours: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def estimated_monthly_cost(self) -> float:
        return self.cost_per_hour * 24 * 30

    def is_underutilized(self, cpu_threshold: float = 10.0, mem_threshold: float = 15.0) -> bool:
        return self.cpu_utilization < cpu_threshold and self.memory_utilization < mem_threshold


class ResourceMonitor:
    """Monitors resources across multiple cloud providers."""

    def __init__(self, config: dict):
        self.config = config
        self.providers = {}
        self._metrics_history: Dict[str, List[ResourceMetrics]] = {}
        self._alerts = []

    async def collect_metrics(self, provider_name: str) -> List[ResourceMetrics]:
        """Collect metrics from a specific provider."""
        provider = self.providers.get(provider_name)
        if not provider:
            raise ValueError(f"Unknown provider: {provider_name}")

        resources = await provider.list_resources()
        metrics = []
        for resource in resources:
            m = await provider.get_metrics(resource["id"])
            metrics.append(ResourceMetrics(
                resource_id=resource["id"],
                provider=provider_name,
                region=resource["region"],
                cpu_utilization=m["cpu"],
                memory_utilization=m["memory"],
                network_in_bytes=m["net_in"],
                network_out_bytes=m["net_out"],
                cost_per_hour=resource.get("cost_per_hour", 0.0),
                uptime_hours=resource.get("uptime_hours", 0.0),
            ))
        return metrics

    async def collect_all(self) -> Dict[str, List[ResourceMetrics]]:
        """Collect metrics from all configured providers."""
        results = {}
        for name in self.providers:
            try:
                results[name] = await self.collect_metrics(name)
                self._metrics_history.setdefault(name, []).extend(results[name])
            except Exception as e:
                logger.error(f"Failed to collect from {name}: {e}")
        return results

    def get_underutilized(self, metrics: Dict[str, List[ResourceMetrics]]) -> List[ResourceMetrics]:
        """Find underutilized resources across all providers."""
        underutilized = []
        for provider_metrics in metrics.values():
            underutilized.extend(m for m in provider_metrics if m.is_underutilized())
        return sorted(underutilized, key=lambda m: m.cost_per_hour, reverse=True)

    def calculate_total_cost(self, metrics: Dict[str, List[ResourceMetrics]]) -> float:
        """Calculate total estimated monthly cost."""
        total = 0.0
        for provider_metrics in metrics.values():
            total += sum(m.estimated_monthly_cost for m in provider_metrics)
        return total
