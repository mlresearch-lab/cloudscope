"""AWS CloudWatch integration."""

import boto3
from .base import BaseProvider


class AWSProvider(BaseProvider):
    """AWS resource monitoring via CloudWatch and Cost Explorer."""

    def __init__(self, credentials: dict, region: str = "us-east-1"):
        super().__init__(credentials, region)
        self.session = boto3.Session(
            aws_access_key_id=credentials.get("access_key"),
            aws_secret_access_key=credentials.get("secret_key"),
            region_name=region,
        )
        self.cloudwatch = self.session.client("cloudwatch")
        self.ec2 = self.session.client("ec2")

    async def list_resources(self):
        instances = self.ec2.describe_instances()
        resources = []
        for reservation in instances["Reservations"]:
            for inst in reservation["Instances"]:
                if inst["State"]["Name"] == "running":
                    resources.append({
                        "id": inst["InstanceId"],
                        "region": self.region,
                        "type": inst["InstanceType"],
                        "cost_per_hour": self._estimate_cost(inst["InstanceType"]),
                    })
        return resources

    async def get_metrics(self, resource_id: str):
        response = self.cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": resource_id}],
            StartTime="...",
            EndTime="...",
            Period=300,
            Statistics=["Average"],
        )
        return {
            "cpu": response["Datapoints"][0]["Average"] if response["Datapoints"] else 0,
            "memory": 0,  # requires CloudWatch agent
            "net_in": 0,
            "net_out": 0,
        }

    async def get_cost_data(self, start_date, end_date):
        ce = self.session.client("ce")
        response = ce.get_cost_and_usage(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
        )
        return {
            r["TimePeriod"]["Start"]: float(r["Total"]["UnblendedCost"]["Amount"])
            for r in response["ResultsByTime"]
        }

    def _estimate_cost(self, instance_type: str) -> float:
        # Simplified pricing lookup
        pricing = {"t3.micro": 0.0104, "t3.small": 0.0208, "t3.medium": 0.0416}
        return pricing.get(instance_type, 0.05)
