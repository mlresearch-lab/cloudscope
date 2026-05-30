"""Cost analysis and optimization recommendations."""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class CostRecommendation:
    resource_id: str
    provider: str
    current_monthly_cost: float
    recommended_action: str
    estimated_savings: float
    confidence: str  # "high", "medium", "low"


class CostAnalyzer:
    """Analyzes cloud spending and generates optimization recommendations."""

    def __init__(self, config: dict):
        self.config = config
        self.thresholds = config.get("thresholds", {
            "cpu_underutilized": 10.0,
            "memory_underutilized": 15.0,
            "idle_hours": 168,  # 1 week
        })

    def analyze(self, metrics_by_provider: dict) -> List[CostRecommendation]:
        recommendations = []
        for provider, metrics_list in metrics_by_provider.items():
            for m in metrics_list:
                recs = self._analyze_resource(m)
                recommendations.extend(recs)
        return sorted(recommendations, key=lambda r: r.estimated_savings, reverse=True)

    def _analyze_resource(self, metrics) -> List[CostRecommendation]:
        recs = []
        if metrics.cpu_utilization < self.thresholds["cpu_underutilized"]:
            recs.append(CostRecommendation(
                resource_id=metrics.resource_id,
                provider=metrics.provider,
                current_monthly_cost=metrics.estimated_monthly_cost,
                recommended_action="Downsize or stop instance",
                estimated_savings=metrics.estimated_monthly_cost * 0.5,
                confidence="high" if metrics.cpu_utilization < 5 else "medium",
            ))
        return recs
