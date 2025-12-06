# Scalability & Performance Strategy

## Target
- Support **1,000,000+ Unique Users/Monitored Entities**.
- High-throughput ingestion (10k+ events/sec).

## Strategies

### 1. Ingestion Layer (Kafka)
- **Partitioning**: Kafka topics will be heavily partitioned (e.g., 50+ partitions for `events-raw`) to allow parallel consumption.
- **Consumer Groups**: Multiple instances of the Spark ingestion job sharing the same Consumer Group ID to load-balance partitions.

### 2. Processing Layer (Spark Streaming)
- **Micro-batching**: Tuned batch intervals (e.g., 500ms - 2s) to balance latency vs throughput.
- **Backpressure**: Spark's `spark.streaming.backpressure.enabled` to prevent OOM during spikes.
- **Scaling**: Kubernetes HPA detects high CPU/Lag and scales Spark Executor pods.

### 3. Vector Database (Qdrant)
- **Distributed Mode**: Sharding collections across multiple Qdrant nodes.
- **Payload Indexing**: Indexing key fields (brand_id, timestamp) avoids full-scan filtering.

### 4. Database & API
- **Read Replicas**: Separate Postgres read replicas for dashboard queries vs write-heavy operational data.
- **Caching**: Redis layer for aggressive caching of aggregated dashboard stats (e.g., "Global Sentiment Last 24h").
- **CDN**: Serve static frontend assets via CDN.

### 5. LLM Inference
- **Batching**: Inference requests are not processed 1-by-1 but batched dynamicallly.
- **Async Queue**: Requests for complex analysis (Crisis Simulation) are sent to a queue (Kafka/RabbitMQ), processed asynchronously, and notified via WebSocket.
