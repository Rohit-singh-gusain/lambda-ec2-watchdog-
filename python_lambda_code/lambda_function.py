
import boto3
import os
from datetime import datetime, timezone


def lambda_handler(event, context):
    region        = os.environ.get("AWS_REGION_NAME", "us-east-1")
    sns_topic_arn = os.environ.get("SNS_TOPIC_ARN")

    ec2 = boto3.client("ec2", region_name=region)
    sns = boto3.client("sns", region_name=region)

    
    response = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            name = "N/A"
            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]
                    break

            launch_time   = instance.get("LaunchTime")
            running_since = "Unknown"
            if launch_time:
                delta         = datetime.now(timezone.utc) - launch_time
                total_seconds = int(delta.total_seconds())
                days          = total_seconds // 86400
                hours         = (total_seconds % 86400) // 3600
                minutes       = (total_seconds % 3600) // 60

                if days > 0:
                    running_since = f"{days}d {hours}h {minutes}m"
                else:
                    running_since = f"{hours}h {minutes}m"

            instances.append({
                "instance_id"   : instance.get("InstanceId",       "N/A"),
                "name"          : name,
                "instance_type" : instance.get("InstanceType",     "N/A"),
                "region"        : region,
                "state"         : instance["State"]["Name"],
                "launch_time"   : launch_time.strftime("%Y-%m-%d %H:%M UTC") if launch_time else "N/A",
                "running_since" : running_since,
                "public_ip"     : instance.get("PublicIpAddress",  "None"),
                "private_ip"    : instance.get("PrivateIpAddress", "None"),
                "az"            : instance.get("Placement", {}).get("AvailabilityZone", "N/A"),
            })

    if instances:
        subject = f"⚠️ EC2 Cost Alert — {len(instances)} instance(s) still running!"
        message = build_alert_message(instances, region)
    else:
        subject = "✅ EC2 Cost Guardian — All Clear, No running instances"
        message = build_clear_message(region)

    sns.publish(
        TopicArn = sns_topic_arn,
        Subject  = subject,
        Message  = message
    )


def build_alert_message(instances, region):
    now   = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = []

    lines.append("=" * 60)
    lines.append("   ⚠️  EC2 COST GUARDIAN — ACTION REQUIRED")
    lines.append("=" * 60)
    lines.append(f"   Checked At  : {now}")
    lines.append(f"   Region      : {region}")
    lines.append(f"   Total Found : {len(instances)} running instance(s)")
    lines.append("=" * 60)

    for i, inst in enumerate(instances, start=1):
        lines.append(f"\n   Instance #{i}")
        lines.append(f"   {'─' * 40}")
        lines.append(f"   Name          : {inst['name']}")
        lines.append(f"   Instance ID   : {inst['instance_id']}")
        lines.append(f"   Type          : {inst['instance_type']}")
        lines.append(f"   Region        : {inst['region']}")
        lines.append(f"   Avail. Zone   : {inst['az']}")
        lines.append(f"   State         : {inst['state'].upper()}")
        lines.append(f"   Running For   : {inst['running_since']}")  
        lines.append(f"   Launched At   : {inst['launch_time']}")
        lines.append(f"   Public IP     : {inst['public_ip']}")
        lines.append(f"   Private IP    : {inst['private_ip']}")

    lines.append("\n" + "=" * 60)
    lines.append("   ACTION REQUIRED:")
    lines.append("   Go to AWS Console → EC2 → Instances")
    lines.append("   Stop or Terminate instances you no longer need")
    lines.append("   to avoid unexpected AWS charges.")
    lines.append("=" * 60)
    lines.append("   Sent by: EC2 Cost Guardian (AWS Lambda)")
    lines.append("=" * 60)

    return "\n".join(lines)


def build_clear_message(region):
    now   = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = []

    lines.append("=" * 60)
    lines.append("   ✅  EC2 COST GUARDIAN — ALL CLEAR")
    lines.append("=" * 60)
    lines.append(f"   Checked At : {now}")
    lines.append(f"   Region     : {region}")
    lines.append("")
    lines.append("   No running EC2 instances found.")
    lines.append("   You are not being charged for any EC2 compute. 🎉")
    lines.append("=" * 60)
    lines.append("   Sent by: EC2 Cost Guardian (AWS Lambda)")
    lines.append("=" * 60)

    return "\n".join(lines)