# Core Concepts

## Portable Memory

Engram is designed to let users move between AI tools without losing continuity. The product goal is that switching from one assistant to another should not require rebuilding context from scratch.

## Knowledge Packs

Knowledge packs are curated bundles of information that can be ingested once and made available everywhere. A knowledge pack might represent:

- framework documentation
- project docs
- company SOPs
- product manuals
- personal reference material

Knowledge packs are intended to be source-aware, versionable, and scopeable.

## Temporal Truth

Engram tracks when information entered the system, when it became effective, when it was last confirmed, and when it was superseded. This lets the system distinguish between:

- current truth
- historical truth
- stale truth

## Memory Lifecycle

Engram should support memory state transitions rather than storing everything forever as flat facts. At minimum:

- active
- stale
- superseded
- archived
- deleted

This is required to prevent bloat and to keep context focused.

## Context Packs

Engram should provide two layers of context:

- a compact always-on state capsule with current work state
- deeper retrieval-backed context packs when a query needs more detail

The system should remain careful about token budget and avoid injecting large blocks of low-value context by default.
