sequenceDiagram
    participant Client
    participant API as FastAPI App
    participant Provider as Alpha Vantage
    participant Kafka as Kafka Broker
    participant Consumer as MA Consumer
    participant DB as PostgreSQL

    Client->>API: GET /prices/latest?symbol=AAPL
    API->>Provider: Fetch price
    Provider-->>API: Return price data
    API->>DB: Save raw market data
    API->>Kafka: Publish price event
    API-->>Client: Return price

    Kafka->>Consumer: Consume price event
    Consumer->>DB: Query last 5 prices
    Consumer->>Consumer: Compute moving average
    Consumer->>DB: Store moving average

