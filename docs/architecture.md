---
config:
  layout: dagre
---

flowchart TB
    Client["Client (Sends Request / Receives Response)"]

    subgraph "Market Data Service"
        API["FastAPI Service"]
        DB[("PostgreSQL")]
    end

    subgraph "Message Queue"
        Producer["Price Producer"]
        Kafka["Apache Kafka"]
        Consumer["MA Consumer"]
        ZK["ZooKeeper"]
    end

    subgraph "External Services"
        MarketAPI["Market Data API (Alpha Vantage)"]
    end

    Client --> API
    API --> MarketAPI
    API --> DB
    API --> Producer
    Producer --> Kafka
    Kafka --> Consumer
    Consumer --> DB
    ZK <--> Kafka
    API --> Client
