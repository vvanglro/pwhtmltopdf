# Playwright HTML to PDF
[![Package version](https://img.shields.io/pypi/v/pwhtmltopdf?color=%2334D058&label=pypi%20package)](https://pypi.python.org/pypi/pwhtmltopdf)

A modern html to pdf scheme based on playwright, Support more html and css technologies.

## Installation

1. Install pwhtmltopdf
    ```sh
   pip install pwhtmltopdf
   ```
2. Install chromium
   ```sh
   playwright install chromium
   ```

## Usage

Simple example:

```python
import asyncio
import pathlib
from pwhtmltopdf import HtmlToPdf


async def this_from_url():
    async with HtmlToPdf() as htp:
        await htp.from_url("https://playwright.dev/", "from_url.pdf")


async def this_from_file():
    async with HtmlToPdf() as htp:
        # Make sure the current directory has a test.html file
        await htp.from_file("test.html", "from_file.pdf")


async def this_from_string():
    async with HtmlToPdf() as htp:
        content = pathlib.Path("test.html").read_text()
        await htp.from_string(content, "from_string.pdf")


if __name__ == '__main__':
    asyncio.run(this_from_url())
```

Render fill:

When `local_render` is equal to true, jinja2 template syntax will be used to render filled html,
If html needs to use local static resources, you need to set `static_root`,
If you want to render filled data dynamically to generate pdf(Based on jinja2), try the following method👇

```python
import asyncio
import pathlib
from pwhtmltopdf import HtmlToPdf


async def this_render_from_url():
    file_path = pathlib.Path("tests/images.html").absolute()
    async with HtmlToPdf(static_root="tests/static",
                         wait_until="load", pdf_kwargs={"print_background": True}) as htp:
        await htp.from_url(
            f"file://{file_path}",
            "tests/effect/from_url/local_url_render.pdf",
            local_render=True,
            char_code=123,
        )


async def this_render_from_file():
    htp = HtmlToPdf(static_root="tests/static")
    await htp.from_file(
        "tests/images.html", "tests/effect/from_file/images_render.pdf",
        local_render=True, char_code=123
    )
    await htp.close()


async def this_render_from_string():
    content = pathlib.Path("tests/images.html").read_text()
    htp = HtmlToPdf(static_root="tests/static")
    await htp.from_string(content, "tests/effect/from_string/images_render.pdf",
                          local_render=True, char_code=123)
    await htp.close()


if __name__ == '__main__':
    asyncio.run(this_render_from_url())
```

## Advanced usage
Support playwright [new_page](https://playwright.dev/python/docs/api/class-browser#browser-new-page) and [page.pdf](https://playwright.dev/python/docs/api/class-page#page-pdf) all parameters passthrough.

```python
import asyncio
from pwhtmltopdf import HtmlToPdf


async def example():
   async with HtmlToPdf(pdf_kwargs={"print_background": True},
                        page_kwargs={"locale": "de-DE", "is_mobile": True}) as htp:
      await htp.from_url("https://playwright.dev/", "from_url.pdf")


if __name__ == '__main__':
   asyncio.run(example())
```
