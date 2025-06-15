
graph TB
   
   subgraph "Message Queue"
        Kafka["Apache Kafka"]
        ZK["ZooKeeper"]
        Producer["Price Producer"]
        Consumer["MA Consumer"]
    end
   
    subgraph "Market Data Service"
        API["FastAPI Service"]
        DB[(PostgreSQL)]
    end
 

    subgraph "External Services"
        MarketAPI["Market Data API (Alpha Vantage)"]
    end
