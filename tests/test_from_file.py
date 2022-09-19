import pytest

from pwhtmltopdf import HtmlToPdf

pytestmark = pytest.mark.asyncio


async def test_from_file():
    htp = HtmlToPdf()
    await htp.from_file("images.html", "effect/from_file/images.pdf")
    await htp.close()


async def test_from_file_render_file_var():
    htp = HtmlToPdf(static_root="static")
    await htp.from_file(
        "images.html",
        "effect/from_file/images_render.pdf",
        local_render=True,
        char_code=123,
    )
    await htp.close()
