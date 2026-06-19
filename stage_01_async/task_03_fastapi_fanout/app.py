"""Task 3 — FastAPI ingestion webhook that fans out 3 async pulls and merges.

This is the front door of the media engine. Something (a feed poller, a "save
this" button, a cron) POSTs a piece of media to ingest; the webhook fans out to
THREE independent async sources concurrently and merges them into one record.

POST /ingest takes a body like:

    {"url": "https://example.com/some-post", "topic": "ai-agents"}

and fans out to:
  - fetch_rss_article(...)        the article body from its RSS/source page
  - parse_youtube_transcript(...) the transcript for any referenced video
  - pull_substack_post(...)       the related Substack/newsletter post

For the scaffold you can SIMULATE each source (sleep + return a dict). The point
isn't real scraping yet — it's the fan-out. All three must run concurrently
(asyncio.gather), and the endpoint merges their results and reports how long the
whole thing took.

The lesson: total latency should be ~max(source latencies), NOT the sum. If you
accidentally `await` them one at a time, the concurrency test in
`tests/test_03_fastapi.py` will catch you.

Implement:
  - three `async def` source functions with different simulated latencies
  - POST /ingest that fans out, merges, and returns
      {"url": ..., "topic": ..., "sources": {...}, "elapsed_seconds": float}
    where `sources` is keyed by source name (rss / youtube / substack)

Run it:
    uv run uvicorn stage_01_async.task_03_fastapi_fanout.app:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Stage 1 — ingestion webhook (fan-out/merge)")


class IngestRequest(BaseModel):
    url: str
    topic: str | None = None


class IngestResponse(BaseModel):
    url: str
    topic: str | None
    sources: dict
    elapsed_seconds: float


async def fetch_rss_article(url: str) -> dict:
    raise NotImplementedError


async def parse_youtube_transcript(url: str) -> dict:
    raise NotImplementedError


async def pull_substack_post(url: str) -> dict:
    raise NotImplementedError


@app.post("/ingest", response_model=IngestResponse)
async def ingest(req: IngestRequest) -> IngestResponse:
    """Fan out to all three sources concurrently, merge them, and time it."""
    raise NotImplementedError
