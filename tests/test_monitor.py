"""Tests for resource monitoring."""

import asyncio
import pytest
from cloudscope.monitor import ResourceMetrics, ResourceMonitor


class TestResourceMetrics:
    def test_estimated_monthly_cost(self):
        m = ResourceMetrics(
            resource_id="i-123", provider="aws", region="us-east-1",
            cpu_utilization=50.0, memory_utilization=60.0,
            network_in_bytes=1000, network_out_bytes=2000,
            cost_per_hour=0.10, uptime_hours=100,
        )
        assert m.estimated_monthly_cost == pytest.approx(72.0)

    def test_is_underutilized(self):
        m = ResourceMetrics(
            resource_id="i-456", provider="aws", region="us-east-1",
            cpu_utilization=5.0, memory_utilization=10.0,
            network_in_bytes=100, network_out_bytes=200,
            cost_per_hour=0.05, uptime_hours=50,
        )
        assert m.is_underutilized() is True

    def test_not_underutilized(self):
        m = ResourceMetrics(
            resource_id="i-789", provider="aws", region="us-east-1",
            cpu_utilization=80.0, memory_utilization=70.0,
            network_in_bytes=10000, network_out_bytes=20000,
            cost_per_hour=0.20, uptime_hours=200,
        )
        assert m.is_underutilized() is False


class TestResourceMonitor:
    def test_calculate_total_cost(self):
        monitor = ResourceMonitor({})
        metrics = {
            "aws": [
                ResourceMetrics(
                    resource_id="i-1", provider="aws", region="us-east-1",
                    cpu_utilization=50, memory_utilization=60,
                    network_in_bytes=1000, network_out_bytes=2000,
                    cost_per_hour=0.10, uptime_hours=100,
                ),
            ],
        }
        assert monitor.calculate_total_cost(metrics) == pytest.approx(72.0)
