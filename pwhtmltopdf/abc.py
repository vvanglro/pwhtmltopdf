import abc
import pathlib
import tempfile
import typing
from types import TracebackType

from jinja2 import Template

from pwhtmltopdf.pw import PlayWrightServer
from pwhtmltopdf.structures import PageParameters, PdfParameters
from pwhtmltopdf.types import StrPath, StrPathLike


class BaseHTP(abc.ABC):
    def __init__(
        self,
        static_root: StrPath = None,
        timeout: typing.Optional[float] = None,
        wait_until: typing.Optional[typing.Literal["commit", "domcontentloaded", "load", "networkidle"]] = None,
        pdf_kwargs: typing.Optional[PdfParameters] = None,
        page_kwargs: typing.Optional[PageParameters] = None,
    ):
        """
        param static_root: The resource directory in html,
                            which is passed in for subsequent rendering.
        """
        self.pw_server = PlayWrightServer(page_kwargs)
        self.static_root = static_root
        self.wait_until = wait_until
        self.timeout = timeout
        self.pdf_kwargs = pdf_kwargs or {}

    async def _page_render(self, url: str, output_path: StrPath = None) -> bytes:
        async with self.pw_server.new_page() as page:
            await page.goto(url, wait_until=self.wait_until, timeout=self.timeout)
            await page.emulate_media(media="print")
            return await page.pdf(
                path=output_path,
                **self.pdf_kwargs,
            )

    async def _content_render(self, content: str, output_path: StrPath = None, **render_kwargs) -> bytes:
        static_path = None
        if self.static_root:
            static_path = pathlib.Path(self.static_root).absolute()
        template = Template(content, enable_async=True)
        if template.debug_info:
            content = await template.render_async(static_path=static_path, **render_kwargs)
        return await self._temp_render(content, output_path)

    async def _temp_render(self, content: str, output_path: StrPath = None) -> bytes:
        with tempfile.NamedTemporaryFile(suffix=".html") as file:
            file.write(content.encode("utf-8"))
            # If the content is too small, it will not write to the disk.
            # Call the write manually.
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

    async def __aenter__(self) -> "BaseHTP":
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[TracebackType],
    ) -> None:
        await self.close()
