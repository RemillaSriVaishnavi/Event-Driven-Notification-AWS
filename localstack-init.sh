#!/bin/bash

echo "Creating SNS Topic..."

aws --endpoint-url=http://localstack:4566 sns create-topic \
--name notification-events \
--region us-east-1

TOPIC_ARN=$(aws --endpoint-url=http://localstack:4566 sns list-topics \
--query "Topics[?contains(TopicArn, 'notification-events')].TopicArn" \
--output text --region us-east-1)

echo "Creating SQS Queue..."

aws --endpoint-url=http://localstack:4566 sqs create-queue \
--queue-name notification-queue \
--region us-east-1

QUEUE_URL=$(aws --endpoint-url=http://localstack:4566 sqs get-queue-url \
--queue-name notification-queue \
--query "QueueUrl" \
--output text --region us-east-1)

QUEUE_ARN=$(aws --endpoint-url=http://localstack:4566 sqs get-queue-attributes \
--queue-url $QUEUE_URL \
--attribute-names QueueArn \
--query "Attributes.QueueArn" \
--output text --region us-east-1)

echo "Subscribing SQS to SNS..."

aws --endpoint-url=http://localstack:4566 sns subscribe \
--topic-arn $TOPIC_ARN \
--protocol sqs \
--notification-endpoint $QUEUE_ARN \
--region us-east-1

echo "SNS ARN: $TOPIC_ARN"
echo "SQS ARN: $QUEUE_ARN"
