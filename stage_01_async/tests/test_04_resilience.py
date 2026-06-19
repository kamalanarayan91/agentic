"""Spec for task 4. These tests define the thresholds your decorators must hit.

Run: uv run pytest stage_01_async/tests/test_04_resilience.py -v
"""

from __future__ import annotations

import asyncio
import time

import pytest

from stage_01_async.task_04_resilience import retry, timeout


async def test_retry_succeeds_on_third_attempt():
    calls = {"n": 0}

    @retry(attempts=3, base_delay=0.0)
    async def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("not yet")
        return "ok"

    assert await flaky() == "ok"
    assert calls["n"] == 3  # exactly 3 calls: 2 failures + 1 success


async def test_retry_gives_up_after_attempts_and_reraises():
    calls = {"n": 0}

    @retry(attempts=3, base_delay=0.0)
    async def always_fails():
        calls["n"] += 1
        raise ValueError("nope")

    with pytest.raises(ValueError):
        await always_fails()
    assert calls["n"] == 3  # not 4 — attempts is the total, off-by-one trap


async def test_retry_only_catches_listed_exceptions():
    calls = {"n": 0}

    @retry(attempts=3, base_delay=0.0, exc=(ValueError,))
    async def wrong_error():
        calls["n"] += 1
        raise KeyError("not retryable")

    with pytest.raises(KeyError):
        await wrong_error()
    assert calls["n"] == 1  # KeyError is not in exc -> no retry


async def test_retry_backoff_timing_is_exponential():
    # 3 attempts, base 0.05 -> sleeps of 0.05 then 0.10 before final failure.
    # Total wall time should be at least the sum of the backoffs.
    @retry(attempts=3, base_delay=0.05)
    async def always_fails():
        raise ValueError("nope")

    start = time.monotonic()
    with pytest.raises(ValueError):
        await always_fails()
    elapsed = time.monotonic() - start
    assert elapsed >= 0.15 - 0.02  # 0.05 + 0.10, small slack


async def test_timeout_fires_when_exceeded():
    @timeout(seconds=0.1)
    async def too_slow():
        await asyncio.sleep(1.0)
        return "never"

    with pytest.raises(asyncio.TimeoutError):
        await too_slow()


async def test_timeout_allows_fast_calls_through():
    @timeout(seconds=0.5)
    async def fast():
        await asyncio.sleep(0.01)
        return "done"

    assert await fast() == "done"
