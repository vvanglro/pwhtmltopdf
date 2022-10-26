import abc
import pathlib
import tempfile

from jinja2 import Template

from pwhtmltopdf.pw import PlayWrightServer
from pwhtmltopdf.types import StrPath, StrPathLike


class BaseHTP(abc.ABC):
    def __init__(self, static_root: StrPath = None):
        """
        param static_root: The resource directory in html, which is passed in for subsequent rendering
        """
        self.pw_server = PlayWrightServer()
        self.static_root = static_root

    async def _page_render(self, url: str, output_path: StrPath = None) -> bytes:
        async with self.pw_server.new_page() as page:
            await page.goto(url, wait_until="load")
            await page.emulate_media(media="print")
            return await page.pdf(path=output_path)

    async def _content_render(
        self, content: str, output_path: StrPath = None, **render_kwargs
    ) -> bytes:
        static_path = None
        if self.static_root:
            static_path = pathlib.Path(self.static_root).absolute()
        template = Template(content, enable_async=True)
        if template.debug_info:
            content = await template.render_async(
                static_path=static_path, **render_kwargs
            )
        return await self._temp_render(content, output_path)

    async def _temp_render(self, content: str, output_path: StrPath = None) -> bytes:
        with tempfile.NamedTemporaryFile(suffix=".html") as file:
            file.write(content.encode("utf-8"))
            # If the content is too small, it will not write to the disk. Call the write manually.
            file.flush()
            url = f"file://{file.name}"
            return await self._page_render(url, output_path)

    @abc.abstractmethod
    async def from_url(
        self,
        url: str,
        output_path: StrPath = None,
        *,
        local_render: bool = False,
        **render_kwargs,
    ) -> bytes:
        ...

    @abc.abstractmethod
    async def from_file(
        self,
        file: StrPathLike,
        output_path: StrPath = None,
        *,
        local_render: bool = False,
        **render_kwargs,
    ) -> bytes:
        ...

    @abc.abstractmethod
    async def from_string(
        self,
        content: str,
        output_path: StrPath = None,
        *,
        local_render: bool = False,
        **render_kwargs,
    ) -> bytes:
        ...

    async def close(self) -> None:
        await self.pw_server.close()
