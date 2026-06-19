"""Task 2 — A from-scratch async HTTP client for media ingestion.

asyncio + aiohttp only. No `requests`, no httpx convenience wrappers, no feed
SDKs (feedparser etc.), no retry libs. The job: pull raw text from RSS feeds and
newsletter/Substack endpoints, many at once, over a single shared session. This
is the ingestion layer's lowest level — everything in later stages sits on top
of it.

Implement two functions with the signatures below. The tests in
`tests/test_02_http_client.py` pin the contract:

  - fetch_text: one GET of a feed/article URL, return the body as str. Raise on
    non-2xx (a dead feed should be loud, not a silently-stored 404 page).
  - fetch_all: pull many feed URLs concurrently over ONE shared session, results
    in the SAME ORDER as the input urls (so you can zip them back to sources).

Things to get right (these are the actual lessons):
  - Create exactly one ClientSession and reuse it (`async with`). Opening a
    session per feed is the #1 beginner mistake — and at ingestion volume it
    will exhaust connections fast.
  - Fan out concurrently — not a for-loop of awaits, which fetches feeds one at a
    time and makes a 50-feed pull take 50x as long. Do it BOTH ways and feel it:
      * asyncio.gather (with return_exceptions to control partial failure), and
      * asyncio.TaskGroup (3.11+, the modern structured-concurrency idiom).
    Then answer in NOTES.md: when one feed raises, what happens to the other 49
    under each approach? Cancellation semantics are where async agents break.
  - Preserve input order in the output. gather does this for you; know why
    (and what you have to do yourself to keep order under TaskGroup).
  - Surface HTTP errors instead of archiving a 500 body as if it were content
    (look at `resp.raise_for_status()`).
"""

from __future__ import annotations

from typing import Sequence


async def fetch_text(session, url: str) -> str:
    """GET a feed/article `url` using the provided aiohttp session; return body text.

    Raise aiohttp.ClientResponseError on a non-2xx status.
    """
    raise NotImplementedError


async def fetch_all(urls: Sequence[str]) -> list[str]:
    """Fetch every feed url concurrently over a single shared session.

    Returns bodies in the same order as `urls`.
    """
    raise NotImplementedError


async def _demo() -> None:
    # A few real feeds/endpoints you can hit while developing.
    feeds = [
        "https://hnrss.org/frontpage",
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://www.theverge.com/rss/index.xml",
    ]
    bodies = await fetch_all(feeds)
    print(f"fetched {len(bodies)} feeds, sizes={[len(b) for b in bodies]}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(_demo())
