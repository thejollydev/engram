# Engram

Portable, local-first memory and context orchestration for AI tools.

Engram is designed for people who use more than one AI assistant and do not want to lose continuity every time they switch tools. It provides a shared memory and knowledge layer that can ingest documents, conversations, and user-managed knowledge packs, then expose the right context to any connected client through a stable API and MCP interface.

## Product Direction

Engram is being built around four core promises:

- Bring your context with you across AI tools.
- Ingest your own knowledge and make it available everywhere.
- Support multiple memory and retrieval strategies instead of locking users into one stack.
- Keep deployment local-first and self-hostable while leaving room for hosted and managed offerings later.

## Core Capabilities

- Shared cross-tool memory for clients such as Claude Code, Codex, Gemini CLI, OpenClaw, and future MCP-compatible tools
- Watched-directory ingestion, with Obsidian as the flagship connector
- Support for multiple memory planes: session, semantic, graph, document, and temporal
- Knowledge packs for injecting curated documentation or domain-specific information into the system
- Hybrid deterministic-first query routing across multiple retrieval providers
- Early support for pluggable providers rather than hard-wiring the product to a single memory engine

## Public Docs

- [Architecture Overview](docs/architecture.md)
- [Core Concepts](docs/concepts.md)
- [Provider Model](docs/providers.md)
- [Public Roadmap](docs/roadmap.md)

Private product planning, enterprise-style architecture documents, and internal implementation notes are maintained outside the public repository.

## Current State

The repository currently contains an early scaffold:

- Docker Compose stack
- custom mem0 image experiments
- an initial vault sync prototype

The architecture is being redesigned so Engram owns the product contract, retrieval orchestration, memory lifecycle, temporal modeling, and provider/plugin system rather than acting as a thin wrapper around third-party tooling.

## Near-Term Goals

- Define the canonical Engram memory model
- Build the multi-plane retrieval architecture
- Ship a local-first API and MCP surface
- Support Obsidian/filesystem ingestion, PDFs, and imported model memories
- Add an early UI for browsing, editing, and managing memories and imports

## License

[Apache License 2.0](LICENSE)
