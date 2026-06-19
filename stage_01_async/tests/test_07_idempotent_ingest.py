"""Spec for the new task 7: at-most-once ingestion with a durable dedup queue.

Run: uv run pytest stage_01_async/tests/test_07_idempotent_ingest.py -v
"""

from __future__ import annotations

import pytest

from stage_01_async.task_07_idempotent_ingest import IdempotentIngestQueue


async def test_processes_a_new_item_once(tmp_path):
    q = IdempotentIngestQueue(tmp_path / "seen.json")
    calls = []

    async def process(item):
        calls.append(item["url"])
        return item["url"].upper()

    result = await q.submit({"url": "https://example.com/a"}, process)
    assert result == "HTTPS://EXAMPLE.COM/A"
    assert calls == ["https://example.com/a"]


async def test_skips_duplicate_in_same_run(tmp_path):
    q = IdempotentIngestQueue(tmp_path / "seen.json")
    calls = []

    async def process(item):
        calls.append(item["url"])
        return "ok"

    await q.submit({"url": "https://example.com/a"}, process)
    await q.submit({"url": "https://example.com/a"}, process)
    assert calls == ["https://example.com/a"]  # process ran exactly once


async def test_url_normalization_collapses_equivalent_urls(tmp_path):
    q = IdempotentIngestQueue(tmp_path / "seen.json")
    calls = []

    async def process(item):
        calls.append(item["url"])
        return "ok"

    # tracking params, fragment, trailing slash, host case -> same article
    await q.submit({"url": "https://Example.com/a/"}, process)
    await q.submit({"url": "https://example.com/a?utm_source=twitter#top"}, process)
    assert len(calls) == 1


async def test_durable_across_process_runs(tmp_path):
    state = tmp_path / "seen.json"

    async def process(item):
        process.n += 1
        return "ok"

    process.n = 0

    # First "run"
    q1 = IdempotentIngestQueue(state)
    await q1.submit({"url": "https://example.com/a"}, process)

    # Fresh queue object simulating a new process start, same state file
    q2 = IdempotentIngestQueue(state)
    await q2.submit({"url": "https://example.com/a"}, process)

    assert process.n == 1  # second run must NOT reprocess
