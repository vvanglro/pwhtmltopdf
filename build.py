import logging
import subprocess


def install_chromium():
    logging.info("\n")
    logging.info("Start downloading the chromium driver")
    subprocess.call("playwright install chromium", shell=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    install_chromium()
