import logging
import subprocess
from typing import Dict, Any


def install_chromium():
    logging.info("\n")
    logging.info("Start downloading the chromium driver")
    subprocess.call("playwright install chromium", shell=True)


def build(setup_kwargs: Dict[str, Any]) -> None:
    install_chromium()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    install_chromium()
