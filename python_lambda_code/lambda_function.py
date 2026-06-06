import boto3
import os

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-east-1')
    sns = boto3.client('sns', region_name='us-east-1')
    sns_topic_arn = os.environ.get("SNS_TOPIC_ARN")

    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])

    if instances:
        message = f"⚠️ {len(instances)} EC2 instance(s) still running:\n" + "\n".join(instances)
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject='EC2 Cost Alert')