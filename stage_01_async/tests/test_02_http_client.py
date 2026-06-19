"""Spec for task 2. Runs a tiny local aiohttp server so the tests are
hermetic — no internet, no flakiness, no rate limits.

Run: uv run pytest stage_01_async/tests/test_02_http_client.py -v
"""

from __future__ import annotations

import asyncio

import pytest
from aiohttp import web

from stage_01_async.task_02_async_http_client import fetch_all, fetch_text


@pytest.fixture
async def server():
    """Spin up a local server returning the path back, with a small delay."""

    async def handler(request: web.Request) -> web.Response:
        await asyncio.sleep(0.1)
        name = request.match_info.get("name", "")
        return web.Response(text=f"hello {name}")

    async def boom(request: web.Request) -> web.Response:
        return web.Response(status=500, text="kaboom")

    app = web.Application()
    app.router.add_get("/echo/{name}", handler)
    app.router.add_get("/boom", boom)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]  # type: ignore[union-attr]
    base = f"http://127.0.0.1:{port}"
    try:
        yield base
    finally:
        await runner.cleanup()


async def test_fetch_all_is_concurrent_and_ordered(server):
    base = server
    urls = [f"{base}/echo/{i}" for i in range(5)]

    start = asyncio.get_event_loop().time()
    bodies = await fetch_all(urls)
    elapsed = asyncio.get_event_loop().time() - start

    # order preserved
    assert bodies == [f"hello {i}" for i in range(5)]
    # 5 requests of 0.1s each, run concurrently, must finish well under 0.5s
    assert elapsed < 0.3


async def test_fetch_text_raises_on_non_2xx(server):
    import aiohttp

    async with aiohttp.ClientSession() as session:
        with pytest.raises(aiohttp.ClientResponseError):
            await fetch_text(session, f"{server}/boom")
