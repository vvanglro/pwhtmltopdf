import pathlib

import pytest

from pwhtmltopdf import HtmlToPdf

pytestmark = pytest.mark.asyncio


async def test_from_url():
    htp = HtmlToPdf()
    await htp.from_url("https://playwright.dev/", "effect/from_url/pw.pdf")
    await htp.close()


async def test_from_url_not_output_path():
    htp = HtmlToPdf()
    pdf_bytes = await htp.from_url("https://playwright.dev/")
    assert isinstance(pdf_bytes, bytes)
    with open("effect/from_url/not_output_path.pdf", "wb") as f:
        f.write(pdf_bytes)
    await htp.close()


async def test_from_local_url():
    file_path = pathlib.Path("images.html").absolute()
    htp = HtmlToPdf()
    await htp.from_url(f"file://{file_path}", "effect/from_url/local_url.pdf")
    await htp.close()


async def test_from_local_url_render():
    file_path = pathlib.Path("images.html").absolute()
    htp = HtmlToPdf(static_root="static")
    await htp.from_url(
        f"file://{file_path}",
        "effect/from_url/local_url_render.pdf",
        local_render=True,
        char_code=123,
    )
    await htp.close()
