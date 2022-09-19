import pathlib

import pytest

from pwhtmltopdf import HtmlToPdf

pytestmark = pytest.mark.asyncio


async def test_from_string_render():
    content = pathlib.Path("images.html").read_text()
    htp = HtmlToPdf(static_root="static")
    await htp.from_string(
        content,
        "effect/from_string/images_render.pdf",
        local_render=True,
        char_code=123,
    )
    await htp.close()


async def test_from_string():
    content = pathlib.Path("images.html").read_text()
    htp = HtmlToPdf()
    await htp.from_string(content, "effect/from_string/images.pdf")
    await htp.close()
