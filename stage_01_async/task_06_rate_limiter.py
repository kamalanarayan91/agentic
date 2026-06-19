"""Task 6 — an ingestion rate-limiter with asyncio.Semaphore.

Sources rate-limit and ban scrapers that hit them too hard. Build a limiter that
caps how many media requests run *at the same time*, then prove it caps
concurrency under a heavy simulated pipeline load (many more feeds queued than
the cap allows in flight).

Implement:
  - class ConcurrencyLimiter(max_concurrency): an async context manager / wrapper
    that never lets more than `max_concurrency` blocks run concurrently.
  - It must expose a way to observe the peak concurrency actually reached, so a
    test can assert peak <= max_concurrency.

Design notes:
  - asyncio.Semaphore(n) is the core. `async with sem:` is the idiom.
  - To *prove* it works you need to measure live concurrency: increment a
    counter on entry, decrement on exit, track the max seen. Do this without a
    race — within a single event loop there's no true parallelism, but you can
    still observe more than N inside the block if your gating is wrong.

The `tests/test_06_rate_limiter.py` spec: launch many more tasks than the limit
with a small sleep inside each, and assert the observed peak never exceeds the
cap (and that, without the limiter, peak would exceed it — i.e. the limiter is
actually doing something).
"""

from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


class ConcurrencyLimiter:
    def __init__(self, max_concurrency: int) -> None:
        # TODO: a semaphore, a live counter, and a peak tracker
        raise NotImplementedError

    @property
    def peak(self) -> int:
        """The maximum number of slots observed in use at once."""
        raise NotImplementedError

    async def run(self, coro_fn: Callable[[], Awaitable[T]]) -> T:
        """Run coro_fn() while holding a slot; release the slot when it finishes."""
        raise NotImplementedError


async def _demo() -> None:
    limiter = ConcurrencyLimiter(max_concurrency=3)

    async def work(i: int) -> int:
        await asyncio.sleep(0.05)
        return i

    results = await asyncio.gather(*(limiter.run(lambda i=i: work(i)) for i in range(20)))
    print(f"ran {len(results)} tasks, peak concurrency = {limiter.peak} (cap was 3)")


if __name__ == "__main__":
    asyncio.run(_demo())
