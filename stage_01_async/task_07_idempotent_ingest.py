"""Task 7 (new) — an idempotent ingestion stage with a durable dedup queue.

Real ingestion pipelines re-see the same article constantly: feeds repeat, the
same story is syndicated to five sources, and your script crashes halfway and
re-runs. Processing the same item twice wastes tokens and pollutes the archive.
This is your Kafka/exactly-once instinct applied to the media engine.

Build a stage that, given a stream of incoming items, fetches+processes each
item AT MOST ONCE — even across separate process runs.

Implement IdempotentIngestQueue with:
  - content_key(item): a stable, content-addressed key. Hash the NORMALIZED url
    (strip tracking params, fragments, trailing slashes, lowercase host) plus,
    if you have it, a hash of the body. Two URLs that point at the same article
    must collapse to one key.
  - async submit(item, process): if this key was already processed (in this run
    OR a previous one), skip and return the cached result/marker. Otherwise run
    `process(item)`, record the key durably, and return the result.
  - Durability: persist seen keys to disk (a json/sqlite file is fine) so a fresh
    process run does NOT re-process what a previous run already did.

The lessons:
  - idempotency is about the KEY, not the timing. Get normalization right or the
    same article leaks through as "new".
  - "at most once" across crashes means you must persist BEFORE you'd lose the
    record — think about ordering of (process, then mark) vs (mark, then process)
    and what each gives you on a mid-run crash.

Make `tests/test_07_idempotent_ingest.py` pass.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable
from pathlib import Path


class IdempotentIngestQueue:
    def __init__(self, state_path: str | Path) -> None:
        # TODO: load previously-seen keys from state_path if it exists
        raise NotImplementedError

    def content_key(self, item: dict[str, Any]) -> str:
        """Stable content-addressed key for an item (normalize the url first)."""
        raise NotImplementedError

    async def submit(
        self,
        item: dict[str, Any],
        process: Callable[[dict[str, Any]], Awaitable[Any]],
    ) -> Any:
        """Process `item` at most once. Skip (and don't call process) if seen."""
        raise NotImplementedError
