# 🏗️ System Architecture - Event Driven Notification System

## Architectural Overview

This project implements an **Event-Driven Microservice Architecture** using AWS messaging services.

The architecture follows an **asynchronous producer-consumer model** where:

- The API Service acts as an **Event Producer**
- AWS SNS acts as an **Event Distributor**
- AWS SQS acts as an **Message Queue**
- Worker Service acts as an **Event Consumer**
- PostgreSQL acts as the **Persistent Storage**

The system ensures decoupling between request handling and background processing.

## High Level Architecture

```
            ┌──────────────┐
            │    Client    │
            └──────┬───────┘
                   │
                   ▼
        ┌────────────────────┐
        │  FastAPI Producer  │
        │   (API Service)    │
        └─────────┬──────────┘
                  │ Publish Event
                  ▼
          ┌──────────────┐
          │  SNS Topic   │
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │  SQS Queue   │
          └──────┬───────┘
                 │ Poll Messages
                 ▼
        ┌────────────────────┐
        │  Worker Service    │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │  PostgreSQL DB     │
        └────────────────────┘
```

## Event Flow

### Step 1: API Request

Client sends notification request to:

```
POST /notify
```

### Step 2: Event Publication

- API Service receives request
- Creates notification payload
- Publishes event to SNS Topic using Boto3 SDK

### Step 3: Event Distribution

- SNS Topic distributes event to all subscribers
- In this system, SQS Queue is subscribed to SNS Topic

### Step 4: Message Queueing

- SNS pushes notification event to SQS Queue
- Queue stores event reliably until consumed

### Step 5: Message Consumption

- Worker Service continuously polls SQS Queue
- Retrieves notification message from queue

### Step 6: Event Processing

Worker:

- Parses message payload
- Converts message into Notification model
- Calls Repository layer

### Step 7: Data Persistence

Repository layer:

- Uses SQLAlchemy ORM
- Stores notification data into PostgreSQL database

### Step 8: Message Deletion

After successful database insertion:

- Worker deletes message from SQS Queue
- Prevents duplicate processing


## Component Interaction

| Component        | Responsibility                     |
|------------------|------------------------------------|
| FastAPI API      | Accept notification request        |
| SNS Topic        | Broadcast notification event       |
| SQS Queue        | Buffer notification messages       |
| Worker Service   | Poll & process messages            |
| SQLAlchemy ORM   | Map Python objects to DB tables    |
| PostgreSQL       | Persist notification data          |
| LocalStack       | Simulate AWS SNS & SQS locally     |

---

## Messaging Design

### SNS Topic

- Used for event broadcasting
- Supports pub-sub architecture
- Enables multiple downstream consumers

### SQS Queue

- Provides message durability
- Guarantees delivery
- Enables asynchronous processing
- Prevents producer-consumer tight coupling


## Database Layer

- PostgreSQL used for persistent storage
- SQLAlchemy ORM handles database interactions
- Notification table stores:

| Column     | Description          |
|------------|----------------------|
| id         | Notification ID      |
| message    | Notification Content |
| created_at | Timestamp            |


## Containerized Deployment

Docker Compose orchestrates:

- API Service Container
- Worker Service Container
- PostgreSQL Container
- LocalStack Container

Ensures:

- Environment consistency
- Service isolation
- Easy local deployment


## Fault Tolerance

System ensures reliability by:

- Using SQS durable message storage
- Processing messages asynchronously
- Deleting messages only after success
- Preventing message loss during failures


## Scalability

The architecture supports horizontal scaling:

- Multiple worker instances can consume messages
- SNS supports multiple subscribers
- SQS distributes load across workers


## Architectural Benefits

- Loose Coupling
- High Scalability
- Asynchronous Processing
- Improved System Resilience
- Reliable Event Handling
- Independent Service Scaling


## Summary

This system successfully demonstrates an event-driven architecture where:

- API produces events
- SNS distributes events
- SQS queues events
- Worker processes events
- PostgreSQL stores results

All components interact asynchronously ensuring scalable and reliable notification processing.
