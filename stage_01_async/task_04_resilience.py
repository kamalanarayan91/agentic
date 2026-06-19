"""Task 4 — media-scraper retry-with-backoff and timeout decorators, by hand.

These wrap the ingestion calls from tasks 2 & 3: a rate-limited scraper should
back off and retry instead of hammering the source, and a hanging feed should
be abandoned rather than blocking the pipeline. Build the primitives generically
here; you'll decorate the real fetchers later.

No tenacity, no backoff library. Two decorators for async functions:

    @retry(attempts=3, base_delay=0.1, exc=(Exception,))
    @timeout(seconds=0.5)

The whole point of this task is the *thresholds*: the tests assert that retry
makes exactly N attempts and that the cumulative backoff matches what you'd
compute by hand, and that timeout fires at the boundary. So be precise about:

  - retry: how many total attempts vs how many retries? (off-by-one trap)
  - backoff: exponential -> delay = base_delay * (2 ** (attempt_index)).
    Sleep between attempts, NOT after the last failure.
  - which exceptions trigger a retry vs propagate immediately.
  - timeout: raise asyncio.TimeoutError when the wrapped coro exceeds `seconds`
    (asyncio.wait_for is the honest tool — use it).

Both decorators must preserve the wrapped function's name/docstring
(functools.wraps) and work on `async def` functions.

Make `tests/test_04_resilience.py` pass.
"""

from __future__ import annotations

from typing import Awaitable, Callable, Type, TypeVar

T = TypeVar("T")


def retry(
    attempts: int = 3,
    base_delay: float = 0.1,
    exc: tuple[Type[BaseException], ...] = (Exception,),
):
    """Retry an async function with exponential backoff.

    - Total tries = `attempts` (so attempts=3 means up to 3 calls).
    - Only retry when the raised exception is an instance of one in `exc`.
    - Re-raise the last exception if all attempts fail.
    - Backoff before retrying: base_delay * 2**i for i = 0, 1, ...
    """

    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        raise NotImplementedError

    return decorator


def timeout(seconds: float):
    """Raise asyncio.TimeoutError if the wrapped coroutine runs longer than `seconds`."""

    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        raise NotImplementedError

    return decorator
