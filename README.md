# blockHouseWorkTrialTask
# Market Data Service – FastAPI Microservice

This service fetches real-time market data, stores it in PostgreSQL, publishes events to Kafka, and processes moving averages.

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo_url>
cd market-data-service
```

### 2. Environment Variables
Create a `.env` file:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/market_data
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```

### 4. Run with Uvicorn (Dev Mode)
```bash
uvicorn app.main:app --reload
```
### 5. Run consumer
python -m scripts.consumer

### 6. Run producer in another Terminal
python -m app.services.kafka.producer

---

## 📌 API Endpoints

### ✅ GET Latest Price
**Endpoint:**
```
GET /prices/latest?symbol=AAPL&provider=alpha_vantage
```
**Sample Response:**
```json
{
  "symbol": "AAPL",
  "price": 196.45,
  "timestamp": "2025-06-15T02:38:16.379478",
  "provider": "alpha_vantage"
}
```

### ✅ POST Polling Job
**Endpoint:**
```
POST /prices/poll
```
**Request Body:**
```json
{
  "symbols": ["AAPL", "MSFT"],
  "interval": 60,
  "provider": "alpha_vantage"
}
```

**Sample Response:**
```json
{
  "job_id": "poll_20250615024308",
  "status": "accepted",
  "config": {
    "symbols": ["AAPL", "MSFT"],
    "interval": 60,
    "provider": "alpha_vantage"
  }
}
```

---

## 📹 Video Walkthrough

[🎥 Watch on Loom](https://www.loom.com/share/42c76ebd47a94d39ace9a3dce02b498c?sid=79bdb495-009e-4fd4-a564-85fff6bce218)

---

## 🧠 Architecture Overview


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


### Flow Diagram
```mermaid
sequenceDiagram
    participant C as Client
    participant A as FastAPI
    participant M as Market API
    participant K as Kafka
    participant MA as MA Consumer
    participant DB as PostgreSQL

    C->>A: GET /prices/latest
    A->>DB: Check cache (if used)
    alt Cache miss
        A->>M: Fetch latest price
        M-->>A: Price data
        A->>DB: Store raw response
        A->>K: Produce price event
    end
    A-->>C: Return price

    K->>MA: Consume price event
    MA->>DB: Fetch last 5 prices
    MA->>MA: Calculate MA
    MA->>DB: Store MA result
```

---



## ✅ Features Completed
- [x] FastAPI REST API (GET / POST)
- [x] PostgreSQL integration
- [x] Kafka producer/consumer
- [x] Moving average calculation
- [x] CI/CD with GitHub Actions
- [x] Linting and Testing
- [x] Docker Compose setup

--
