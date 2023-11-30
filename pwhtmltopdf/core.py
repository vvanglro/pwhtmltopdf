import pathlib
import typing

from pwhtmltopdf.abc import BaseHTP
from pwhtmltopdf.structures import PageParameters, PdfParameters
from pwhtmltopdf.types import StrPath, StrPathLike


class HtmlToPdf(BaseHTP):
    def __init__(
        self,
        static_root: StrPath = None,
        timeout: typing.Optional[float] = None,
        wait_until: typing.Optional[typing.Literal["commit", "domcontentloaded", "load", "networkidle"]] = None,
        page_kwargs: typing.Optional[PageParameters] = None,
        pdf_kwargs: typing.Optional[PdfParameters] = None,
    ):
        super().__init__(
            static_root=static_root,
            wait_until=wait_until,
            timeout=timeout,
            pdf_kwargs=pdf_kwargs,
            page_kwargs=page_kwargs,
        )

    async def from_url(
        self,
        url: str,
        output_path: StrPath = None,
        *,
        local_render: bool = False,
        **render_kwargs,
    ) -> bytes:
        if url.startswith("file://") and local_render:
            return await self.from_file(url[7:], output_path, local_render=True, **render_kwargs)
        return await self._page_render(url, output_path)

    async def from_file(
        self,
        file: StrPathLike,
        output_path: StrPath = None,
        *,
        local_render: bool = False,
        **render_kwargs,
    ) -> bytes:
        if local_render:
            content = pathlib.Path(file).read_text()
            return await self._content_render(content, output_path, **render_kwargs)
        else:
            url = f"file://{pathlib.Path(file).absolute()}"
            return await self._page_render(url, output_path)

    async def from_string(
        self,
        content: str,
        output_path: StrPath = None,
        *,
        local_render: bool = False,
        **render_kwargs,
    ) -> bytes:
        if local_render:
            return await self._content_render(content, output_path, **render_kwargs)
        else:
            return await self._temp_render(content, output_path)
