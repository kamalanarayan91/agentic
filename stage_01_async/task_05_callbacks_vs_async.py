"""Task 5 — the same ingestion pipeline, two ways: callbacks vs async/await.

The pipeline (keep it identical across both implementations so the comparison
is fair) — a small dependency chain like the real ingest path:

    1. "fetch" a feed's article list for a source      (simulated I/O, ~0.1s)
    2. using the first item, "fetch" that article's body   (depends on step 1)
    3. using the body, "extract" its key links/metadata    (depends on step 2)
    4. merge {body + extracted} into one content record and return it

Both versions should simulate I/O latency (e.g. a sleep) so the control-flow
differences actually show up.

Implement BOTH:
  - run_with_callbacks(...): no async/await. Model it the way the toy loop in
    task 1 works — pass continuations (callbacks) that fire when each step's
    "I/O" completes. You can drive it with your EventLoop from task 1, or with
    threading.Timer, or a plain callback chain. The pain is the point.
  - run_with_async(...): the same DAG written with async/await.

Then fill in the WRITE-UP below: exactly 3 sentences naming which *classes of
bug* each style makes easier to introduce. Be specific (e.g. "callback version
makes it easy to forget the error path because there's no single place errors
propagate to" — but in your own words, from what you actually hit).
"""

from __future__ import annotations

from typing import Any, Callable


def run_with_callbacks(source: str, on_done: Callable[[dict[str, Any]], None]) -> None:
    """Callback-style: calls on_done(record) when the whole chain finishes."""
    raise NotImplementedError


async def run_with_async(source: str) -> dict[str, Any]:
    """Async/await-style: returns the merged content record."""
    raise NotImplementedError


# =============================================================================
# WRITE-UP (3 sentences). Fill this in AFTER implementing both versions.
# =============================================================================
WRITEUP = """
TODO: 3 sentences.
1.
2.
3.
"""
