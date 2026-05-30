# CloudScope

Multi-cloud resource monitor and cost optimizer.

## Features

- **Multi-cloud monitoring** — AWS, GCP, Azure from a single CLI
- **Cost analysis** — Breakdown by provider, region, service
- **Optimization recommendations** — Identify underutilized resources
- **Alerting** — Slack/webhook notifications for cost anomalies
- **Scheduling** — Automated daily/weekly reports

## Quick Start

```bash
pip install cloudscope
cloudscope scan --config cloudscope.json
```

## Configuration

```json
{
  "providers": {
    "aws": {
      "access_key": "AKIA...",
      "secret_key": "...",
      "region": "us-east-1"
    }
  },
  "thresholds": {
    "cpu_underutilized": 10.0,
    "memory_underutilized": 15.0
  }
}
```

## Commands

```bash
cloudscope scan              # Scan all resources
cloudscope cost              # Cost breakdown
cloudscope optimize          # Optimization recommendations
cloudscope scan -p aws       # Scan specific provider
```

## Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
