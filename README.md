# Engram

Self-hosted AI memory stack for persistent, cross-tool memory. Built on [mem0](https://github.com/mem0ai/mem0) with pgvector for semantic search, Neo4j for graph memory, and an Obsidian vault sync daemon.

## What It Does

Engram gives your AI tools (Claude Code, Gemini CLI, Codex CLI, OpenClaw, or anything with REST/MCP access) a shared, persistent memory layer. Notes you write in Obsidian are automatically ingested. Conversations and context accumulate across tools and sessions.

**Components:**

| Service | Role |
|---------|------|
| **mem0 API server** | Memory extraction, retrieval, and orchestration (REST API) |
| **pgvector (PostgreSQL)** | Vector store for semantic similarity search |
| **Neo4j + APOC** | Knowledge graph for entity relationships and context chains |
| **vault-sync** | Watches an Obsidian vault (or any markdown directory) and ingests changes into mem0 |

## Architecture

```
Your AI Tools (Claude Code, Gemini CLI, Codex, OpenClaw, etc.)
        │
        ├── REST API (:8000)
        │   └── mem0 API server
        │       ├── pgvector (PostgreSQL) — vector embeddings
        │       └── Neo4j + APOC — knowledge graph
        │
        └── MCP (via mem0-mcp-selfhosted or similar adapter)

Obsidian Vault (or any markdown directory)
        │
        └── vault-sync daemon (watchdog) → mem0 API → stored as memories
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- An Ollama instance (or OpenAI API key) for LLM + embeddings

### 1. Clone and configure

```bash
git clone https://github.com/thejollydev/engram.git
cd engram
cp .env.example .env
# Edit .env with your passwords and Ollama URL
```

### 2. Start the stack

```bash
docker compose up -d
```

### 3. Configure mem0 for your LLM provider

After the stack is healthy, configure Ollama (or your preferred provider):

```bash
curl -s -X POST http://localhost:8000/configure \
  -H "Content-Type: application/json" \
  -d @mem0-config.json
```

See [`mem0-config.json.example`](mem0-config.json.example) for the full configuration template.

### 4. Verify

```bash
# Check all services are healthy
docker compose ps

# Test the API
curl -s http://localhost:8000/memories?user_id=default

# Swagger docs
open http://localhost:8000/docs
```

### 5. (Optional) Point vault-sync at your Obsidian vault

Set `VAULT_PATH` in `.env` to your vault directory. The vault-sync daemon will do a bulk ingest on startup, then watch for changes.

## Configuration

All configuration is done through `.env` and the `POST /configure` endpoint. See:

- [`.env.example`](.env.example) — environment variables for Docker Compose
- [`mem0-config.json.example`](mem0-config.json.example) — mem0 runtime configuration (LLM, embedder, graph store)

## MCP Integration

The mem0 API server exposes a REST API only — it does not natively serve MCP. To connect MCP-compatible tools (Claude Code, Gemini CLI, etc.), use a community MCP adapter such as [`mem0-mcp-selfhosted`](https://github.com/elvismdev/mem0-mcp-selfhosted).

## API Reference

The mem0 API runs on port 8000. Key endpoints:

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/configure` | Set LLM, embedder, vector store, graph store config |
| POST | `/memories` | Create memories |
| GET | `/memories` | List memories (filter by `user_id`, `agent_id`) |
| POST | `/search` | Semantic memory search |
| DELETE | `/memories/{id}` | Delete a memory |
| GET | `/docs` | Swagger/OpenAPI explorer |

## Project Structure

```
engram/
├── docker-compose.yml          # Full stack orchestration
├── .env.example                # Environment variable template
├── mem0-config.json.example    # mem0 runtime config template
├── mem0-custom/
│   └── Dockerfile              # Custom mem0 image with graph memory deps
└── vault-sync/
    ├── Dockerfile
    ├── requirements.txt
    └── sync.py                 # Obsidian vault watcher + mem0 ingestion
```

## License

[Apache License 2.0](LICENSE)
