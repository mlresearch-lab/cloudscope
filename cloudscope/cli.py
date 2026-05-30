"""Command-line interface for CloudScope."""

import argparse
import asyncio
import json
import sys
from .monitor import ResourceMonitor
from .cost_analyzer import CostAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Multi-cloud resource monitor")
    parser.add_argument("--config", "-c", default="cloudscope.json", help="Config file path")
    parser.add_argument("--format", "-f", choices=["json", "table", "csv"], default="table")
    parser.add_argument("--provider", "-p", help="Specific provider to query")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("scan", help="Scan all resources")
    sub.add_parser("cost", help="Show cost breakdown")
    sub.add_parser("optimize", help="Show optimization recommendations")

    args = parser.parse_args()
    asyncio.run(_run(args))

async def _run(args):
    with open(args.config) as f:
        config = json.load(f)

    monitor = ResourceMonitor(config)
    if args.command == "scan":
        metrics = await monitor.collect_all()
        print(f"Found {sum(len(v) for v in metrics.values())} resources")
    elif args.command == "cost":
        metrics = await monitor.collect_all()
        total = monitor.calculate_total_cost(metrics)
        print(f"Estimated monthly cost: ${total:,.2f}")
    elif args.command == "optimize":
        metrics = await monitor.collect_all()
        analyzer = CostAnalyzer(config)
        recs = analyzer.analyze(metrics)
        for r in recs:
            print(f"  {r.resource_id}: {r.recommended_action} (save ${r.estimated_savings:.2f}/mo)")


if __name__ == "__main__":
    main()
