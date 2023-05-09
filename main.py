import logging
import logging.handlers
import os

import re
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    firebolt = requests.get('https://www.fireboltt.com/products/king?variant=42334775640255')
    if firebolt.status_code == 200:
        soup= BeautifulSoup(firebolt.content,'html.parser')
        content = soup.find_all(class_='money')
        content = str(content)
        re_prices = '(₹.*?)<\/span>'
        price_list = re.findall(re_prices, content)
        logger.info(f"Today's price: {price_list[0]}")