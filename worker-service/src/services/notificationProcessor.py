import boto3
import os
import json
import time
from src.models.notificationRepo import save_notification

sqs = boto3.client(
    "sqs",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

QUEUE_URL = "http://localstack:4566/000000000000/notification-queue"

def poll_messages():
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20
            )

            messages = response.get("Messages", [])

            for message in messages:
                body = json.loads(message["Body"])
                event = json.loads(body["Message"])

                print("Processing:", event)

                if event["eventType"] == "UserRegisteredEvent":
                    messageContent = f"Welcome Email sent to {event['payload']['email']}"
                    notificationType = "Welcome Email"

                elif event["eventType"] == "OrderPlacedEvent":
                    messageContent = f"Order Confirmation sent"
                    notificationType = "Order Confirmation"

                save_notification(
                    event["eventId"],
                    event["payload"].get("user_id"),
                    notificationType,
                    messageContent
                )

                sqs.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=message["ReceiptHandle"]
                )

        except Exception as e:
            print("Error:", e)

        time.sleep(5)
