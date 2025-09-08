# Embedding Service

A high-performance text embedding service built with FastEmbed and Flask. Converts text into 384-dimensional vectors for semantic search.

## Features

- **Fast**: ~50ms embedding generation
- **Self-Hosted**: No API limits or external dependencies
- **Docker Ready**: Easy deployment with health checks
- **384 Dimensions**: BAAI/bge-small-en-v1.5 model
- **Production Ready**: Built with Gunicorn and error handling

## Quick Start

```bash
# Using Docker (Recommended)
docker-compose up -d

# Manual installation
pip install -r requirements.txt
python main.py
```

## API Usage

```bash
# Generate embedding
curl -X POST http://localhost:5000/embed \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'

# Health check
curl http://localhost:5000/health
```

**Response:**
```json
{
  "embedding": [0.015, -0.022, 0.008, ...],
  "dimensions": 384,
  "model": "fastembed"
}
```

## Performance

- **Speed**: ~50ms per request
- **Throughput**: ~20 req/sec
- **Memory**: ~200MB
- **Model Size**: 20MB

## Docker

```yaml
services:
  embedding-service:
    build: .
    ports:
      - "5000:5000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
```

## Requirements
```
fastembed==0.2.6
flask==3.0.0
gunicorn==21.2.0
```

---

**Built for high-performance semantic search**