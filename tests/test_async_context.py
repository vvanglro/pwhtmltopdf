import pytest

from pwhtmltopdf import HtmlToPdf

pytestmark = pytest.mark.asyncio


async def test_async_enter_exit():
    async with HtmlToPdf() as htp:
        ...
    assert htp.pw_server.server is None
    assert htp.pw_server.browser is None


async def test_async_enter_exit_from_file():
    async with HtmlToPdf(wait_until="load", pdf_kwargs={"print_background": True}) as htp:
        await htp.from_file("images.html", "effect/from_file/async_enter_exit_images.pdf")
    assert htp.pw_server.server is None
    assert htp.pw_server.browser is None
