"""Spec for task 6: prove the Semaphore actually caps concurrency under load.

Run: uv run pytest stage_01_async/tests/test_06_rate_limiter.py -v
"""

from __future__ import annotations

import asyncio

from stage_01_async.task_06_rate_limiter import ConcurrencyLimiter


async def test_limiter_caps_peak_concurrency():
    limiter = ConcurrencyLimiter(max_concurrency=3)

    async def work():
        await asyncio.sleep(0.05)

    # Launch 20 tasks against a cap of 3.
    await asyncio.gather(*(limiter.run(work) for _ in range(20)))

    assert limiter.peak <= 3
    assert limiter.peak == 3  # under this load it SHOULD saturate the cap


async def test_without_limiter_peak_would_exceed_cap():
    # Control: the same workload with no gating reaches much higher concurrency.
    live = {"n": 0, "peak": 0}

    async def work():
        live["n"] += 1
        live["peak"] = max(live["peak"], live["n"])
        await asyncio.sleep(0.05)
        live["n"] -= 1

    await asyncio.gather(*(work() for _ in range(20)))
    assert live["peak"] > 3  # proves the limiter in the other test is doing real work
