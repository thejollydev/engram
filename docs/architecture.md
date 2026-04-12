# Architecture Overview

## What Engram Is

Engram is a memory orchestration layer for AI systems. It sits between AI clients and multiple memory or retrieval backends, giving users one place to ingest knowledge, manage memory, and provide context across tools.

## Architecture Shape

Engram is organized around six major subsystems:

1. `engram-api`
   Public API for ingestion, retrieval, memory lifecycle management, and context-pack generation.
2. `engram-mcp`
   MCP server that exposes Engram capabilities to AI tools.
3. `engram-ingest`
   Connectors and importers for watched directories, Obsidian, PDFs, chat exports, and future managed sources.
4. `engram-retrieval`
   Hybrid deterministic-first router that chooses which memory planes and providers to query.
5. `engram-context`
   Builds compact always-on state capsules plus deeper on-demand context packs.
6. `engram-ui`
   Web interface for browsing memories, editing state, managing imports, and inspecting context.

## Memory Planes

Engram is intentionally multi-plane:

- Session memory: current work and handoff continuity
- Semantic memory: distilled long-lived facts, preferences, and decisions
- Graph memory: entities and relationships
- Document memory: source-grounded retrieval from documents and knowledge packs
- Temporal memory: timestamps, supersession, freshness, and historical truth

## Retrieval Strategy

Engram uses a hybrid deterministic-first router.

- Queries are classified by intent.
- The most likely planes and providers are searched first.
- Broader fallback search is used when confidence is low.
- Results are merged, reranked, and returned with provenance.

This avoids querying everything all the time while still allowing broader recovery when needed.

## Product Philosophy

Engram is not meant to force a single backend choice. It should support defaults while allowing users to choose alternatives for:

- document retrieval
- graph storage
- semantic retrieval
- embedding models
- rerankers
- ingestion connectors

That modularity is part of the product identity, not just an implementation detail.
