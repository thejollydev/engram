# Provider Model

## Why Providers Exist

Engram is intended to be a product, not a wrapper around one backend. To reduce lock-in and allow different deployment profiles, Engram should treat storage and retrieval systems as providers behind a stable product contract.

## Provider Categories

- Semantic retrieval providers
- Graph providers
- Document providers
- Embedding providers
- Reranking providers
- Import/connectors

## Initial Direction

The public architecture currently assumes:

- a default semantic stack centered on PostgreSQL plus pgvector
- an early graph provider
- a native document provider fallback
- an early PageIndex provider for reasoning-based document retrieval

## Design Goal

Every provider category should have:

- a sensible default
- a documented interface
- at least one alternative as early as practical

This supports the long-term product idea of “choose your own stack” while still giving users a default path that works.

## Product Boundary

Providers should not define Engram’s public contract. Engram should own:

- memory schema
- lifecycle rules
- routing logic
- context-pack assembly
- provenance model
- client-facing API and MCP behavior
