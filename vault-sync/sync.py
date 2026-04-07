#!/usr/bin/env python3
"""vault-sync: Watch a markdown directory for changes and ingest into mem0."""

import os
import time
import httpx
import frontmatter
import structlog
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

log = structlog.get_logger()

VAULT_PATH = Path(os.environ.get("VAULT_PATH", "/vault"))
MEM0_URL = os.environ.get("MEM0_API_URL", "http://mem0:8000")
USER_ID = os.environ.get("USER_ID", "default")
CHUNK_CHARS = int(os.environ.get("CHUNK_CHARS", "3000"))

# Directories and files to skip during ingestion.
# Customize via comma-separated env vars.
IGNORE_DIRS = set(
    os.environ.get("IGNORE_DIRS", ".obsidian,.trash,.git,.trash-http-mcp").split(",")
)
IGNORE_FILES = set(
    os.environ.get("IGNORE_FILES", "").split(",")
) - {""}


def is_ignored(path: Path) -> bool:
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
    return path.name in IGNORE_FILES


def chunk_text(text: str) -> list[str]:
    chunks = []
    while len(text) > CHUNK_CHARS:
        split_at = text.rfind("\n", 0, CHUNK_CHARS)
        if split_at == -1:
            split_at = CHUNK_CHARS
        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()
    if text:
        chunks.append(text)
    return chunks


def ingest(path: Path, client: httpx.Client):
    if is_ignored(path):
        return
    try:
        post = frontmatter.load(str(path))
        content = post.content.strip()
        if not content:
            return
        title = post.get("title", path.stem)
        rel = str(path.relative_to(VAULT_PATH))
        metadata = {"source_file": rel, "note_title": title, "tags": post.get("tags", [])}
        for i, chunk in enumerate(chunk_text(content)):
            client.post(
                "/memories",
                json={
                    "messages": [{"role": "user", "content": f"[{title}]\n{chunk}"}],
                    "user_id": USER_ID,
                    "metadata": {**metadata, "chunk_index": i},
                },
                timeout=30,
            )
        log.info("ingested", file=rel, chunks=i + 1)
    except Exception as e:
        log.error("ingest_failed", file=str(path), error=str(e))


class VaultHandler(FileSystemEventHandler):
    def __init__(self):
        self.client = httpx.Client(base_url=MEM0_URL)

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".md"):
            return
        ingest(Path(event.src_path), self.client)

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".md"):
            return
        ingest(Path(event.src_path), self.client)

    def on_deleted(self, event):
        if event.is_directory or not event.src_path.endswith(".md"):
            return
        log.info("deleted", file=event.src_path)


if __name__ == "__main__":
    log.info("vault-sync starting", vault=str(VAULT_PATH), mem0=MEM0_URL)
    client = httpx.Client(base_url=MEM0_URL)
    log.info("bulk ingest starting")
    for md_file in VAULT_PATH.rglob("*.md"):
        ingest(md_file, client)
    log.info("bulk ingest complete")

    handler = VaultHandler()
    observer = Observer()
    observer.schedule(handler, str(VAULT_PATH), recursive=True)
    observer.start()
    log.info("watching vault for changes")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
