"""Task 1 — A toy event loop in ~80 lines.

Goal: build the *why* of async before you ever `import asyncio`. An event loop
is just a queue of callbacks plus a clock. There is no magic.

You will implement a single-threaded cooperative loop that supports:

    loop.call_soon(fn)          -> schedule fn() to run on the next tick
    loop.call_later(delay, fn)  -> schedule fn() to run after `delay` seconds
    loop.run()                  -> drain the loop until nothing is left to do

There are NO coroutines here on purpose. This is the callback-based substrate
that async/await is sugar over. (You'll feel the pain of callbacks in task 5.)

Mental model:
  - Keep a "ready" queue of callbacks to run now.
  - Keep a "scheduled" min-heap of (when, callback) for timers.
  - Each tick: move any timers whose time has come into ready, run all ready
    callbacks. If ready is empty but timers remain, sleep until the next timer.
  - Stop when both are empty.

Implementation hints (don't peek unless stuck):
  - `time.monotonic()` for the clock, `heapq` for the timer queue.
  - Run only the callbacks that were ready at the *start* of the tick, so a
    callback scheduling another callback doesn't starve the loop.

Self-check: run this file. The prints must come out in this order:
    start
    soon-1
    soon-2
    later-100ms
    later-200ms
    done
"""

from __future__ import annotations

import heapq
import itertools
import time
import collections
from typing import Callable


class EventLoop:
    def __init__(self) -> None:
        # TODO: a FIFO of callbacks ready to run now
        # TODO: a min-heap of scheduled timers: (when, tiebreak, callback)
        # TODO: a counter for stable ordering of equal timestamps
        self.queue = collections.deque()
        self.heap = []
        self.counter = itertools.count()

    def call_soon(self, callback: Callable[[], None]) -> None:
        """Schedule `callback` to run on the next tick."""
        self.queue.append(callback)
        

    def call_later(self, delay: float, callback: Callable[[], None]) -> None:
        next_time = time.monotonic() + delay
        heapq.heappush(self.heap, (next_time, next(self.counter), callback))

    def run(self) -> None:
        while self.queue or self.heap:
            now = time.monotonic()
            
            while self.heap and self.heap[0][0] >= now:
                self.call_soon(heapq.heappop(self.heap)[2])
            
            if not self.queue and self.heap:
                sleep_time = self.heap[0][0] - time.monotonic()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                continue

            num_ticks = len(self.queue)
            for _ in range(num_ticks):
                self.queue.popleft()()
        


def _self_check() -> None:
    loop = EventLoop()

    print("start")
    loop.call_soon(lambda: print("soon-1"))
    loop.call_soon(lambda: print("soon-2"))
    loop.call_later(0.2, lambda: print("later-200ms"))
    loop.call_later(0.1, lambda: print("later-100ms"))
    loop.call_later(0.3, lambda: print("done"))
    loop.run()


if __name__ == "__main__":
    _self_check()
