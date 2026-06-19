# Stage 1 — Async Foundations

> The mechanical layer everything else runs on. Media ingestion is high-volume
> and heavily blocked by network I/O — don't skip concurrency.

The running theme for this stage is the **media engine's ingestion layer**:
pulling RSS feeds, newsletter pages, YouTube transcripts and Substack posts
concurrently, surviving rate-limited and hanging scrapers. The async mechanics
are the real lesson; the media framing is just so the work matches the project
you're building toward (see `../CURRICULUM.md`).

## How this scaffold works

Each task has a stub module with a docstring contract and `NotImplementedError`
where your code goes. Where it makes sense, there's a **failing test that is the
spec** — make it pass. Nothing here is implemented for you on purpose. Read the
contract, write the code, run the test.

```bash
# install deps (once)
uv sync

# run everything
uv run pytest

# run one task's tests
uv run pytest stage_01_async/tests/test_04_resilience.py -v

# run a script-style task directly
uv run python stage_01_async/task_01_toy_event_loop.py
uv run python stage_01_async/task_06_rate_limiter.py

# the FastAPI app (task 03)
uv run uvicorn stage_01_async.task_03_fastapi_fanout.app:app --reload
```

## The 7 tasks

| # | File | What you're proving | Has tests? |
|---|------|---------------------|------------|
| 1 | `task_01_toy_event_loop.py` | You understand what an event loop *is* before using one | self-check `__main__` |
| 2 | `task_02_async_http_client.py` | Raw aiohttp pulling RSS/newsletter text concurrently, no wrapper SDKs | `tests/test_02_http_client.py` |
| 3 | `task_03_fastapi_fanout/app.py` | Ingestion webhook fans out to RSS + YouTube + Substack and merges | `tests/test_03_fastapi.py` |
| 4 | `task_04_resilience.py` | Scraper retry+backoff and timeout decorators fire at the right thresholds | `tests/test_04_resilience.py` |
| 5 | `task_05_callbacks_vs_async.py` | Same ingestion pipeline two ways; you can name the bug classes each invites | write-up in file |
| 6 | `task_06_rate_limiter.py` | A Semaphore actually caps concurrent media requests under load | `tests/test_06_rate_limiter.py` |
| 7 | `tests/test_03_fastapi.py` | pytest-asyncio integration incl. a deliberate timeout on a hanging scraper | (that file) |

## Suggested order

1 → 4 → 6 → 2 → 3 → 7 → 5. Build the primitives (loop, decorators, limiter)
before the I/O-bound ones, and do the callbacks-vs-async write-up last when you
have the most async intuition to compare against.

## Definition of done for the stage

- [ ] `uv run pytest` is green
- [ ] task 01 self-check prints in the right order
- [ ] task 05 write-up paragraph filled in
- [ ] You filled in `NOTES.md` with at least the "what clicked" line per task
