"""Spec for task 3 + task 7: integration tests for the ingestion webhook via
pytest-asyncio, including one test that intentionally times out on a hanging
web scraper.

Uses httpx.ASGITransport so the app is exercised in-process (no running server).

Run: uv run pytest stage_01_async/tests/test_03_fastapi.py -v
"""

from __future__ import annotations

import asyncio

import httpx
import pytest

from stage_01_async.task_03_fastapi_fanout.app import app


def _client() -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")


async def test_ingest_returns_merged_sources():
    async with _client() as client:
        resp = await client.post(
            "/ingest", json={"url": "https://example.com/post", "topic": "ai-agents"}
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["url"] == "https://example.com/post"
    assert body["topic"] == "ai-agents"
    # all three sources (rss + youtube + substack) must have contributed
    assert len(body["sources"]) == 3


async def test_ingest_runs_sources_concurrently():
    # If the webhook fans out correctly, total time ~= the slowest source,
    # not the sum. Give generous headroom but enough to catch sequential awaits.
    async with _client() as client:
        resp = await client.post("/ingest", json={"url": "https://example.com/timing"})
    body = resp.json()
    # Tune these to your simulated source sleeps. Default assumption: slowest
    # ~0.3s, sum ~0.6s. Concurrent execution must land well under the sum.
    assert body["elapsed_seconds"] < 0.5


async def test_hanging_scraper_times_out():
    # Required by the curriculum: a test that intentionally times out on a
    # hanging web scraper. We wrap the request in an absurdly tight deadline so
    # a slow/hanging ingest surfaces as asyncio.TimeoutError instead of blocking
    # the pipeline forever.
    async with _client() as client:
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(
                client.post("/ingest", json={"url": "https://example.com/hangs"}),
                timeout=0.001,  # tighter than any real source -> must raise
            )
