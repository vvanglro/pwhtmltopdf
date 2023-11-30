import asyncio
import contextlib
from typing import AsyncGenerator, Optional

from playwright.async_api import Browser, Page, async_playwright
from playwright.async_api import Playwright as AsyncPlaywright


class PlayWrightServer:
    def __init__(self, page_kwargs):
        self.__browser_lock = asyncio.Lock()
        self.server: Optional["AsyncPlaywright"] = None
        self.browser: Optional["Browser"] = None
        self.page_kwargs = page_kwargs or {}

    @contextlib.asynccontextmanager
    async def new_page(self) -> AsyncGenerator["Page", None]:
        page = None
        try:
            async with self.__browser_lock:
                if self.browser is None:
                    self.server = await async_playwright().start()
                    self.browser = await self.server.chromium.launch()
            page = await self.browser.new_page(**self.page_kwargs)
            yield page
        finally:
            if page is not None:
                await page.close()

    async def close(self) -> None:
        if self.browser is not None:
            await self.browser.close()
            self.browser = None
        if self.server is not None:
            await self.server.stop()  # type: ignore
            self.server = None
