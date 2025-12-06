# API Documentation

## Overview
The Sentiment Analysis Platform exposes a REST API and WebSocket interfaces.

## Standards
- **Spec**: OpenAPI 3.0
- **Format**: JSON
- **Base URL**: `/api/v1`

## Specification (Swagger/OpenAPI)

The full interactive documentation is available at `/docs` when the backend is running.

### Core Endpoints

#### Authentication
- `POST /auth/token`: Get JWT access token.

#### Analytics
- `GET /analytics/summary`: Get aggregated dashboard stats (brand health, total mentions).
    - Params: `time_range` (1h, 24h, 7d), `brand_id`
- `GET /analytics/sentiment-trend`: Time-series data for sentiment (0.0 to 1.0).
- `GET /analytics/geo-distribution`: Heatmap data for mentions.

#### Feed
- `GET /feed/live`: Get latest analyzed items (Paginated).

#### Management
- `POST /config/keywords`: detailed keywords to track.
- `GET /config/alerts`: Configure alert thresholds (e.g., "Notify if sentiment drops below 0.3").

## WebSockets
**Endpoint**: `/ws/live`

**Protocol**:
Server pushes JSON events when new high-priority analysis is complete or stats update.

```json
{
  "type": "ALERT",
  "data": {
    "level": "CRITICAL",
    "message": "Sudden spike in negative sentiment detected for keyword: 'Login'",
    "timestamp": "2023-10-27T10:00:00Z"
  }
}
```
