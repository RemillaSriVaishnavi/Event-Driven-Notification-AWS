import boto3
import os
import json
import uuid
from datetime import datetime

sns_client = boto3.client(
    "sns",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

def publish_event(event_type, payload):
    event = {
        "eventId": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "eventType": event_type,
        "payload": payload
    }

    response = sns_client.publish(
        TopicArn=TOPIC_ARN,
        Message=json.dumps(event),
        MessageAttributes={
            'eventType': {
                'DataType': 'String',
                'StringValue': event_type
            }
        }
    )

    print(f"Event Published: {response['MessageId']}")
    return response
