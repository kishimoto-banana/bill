import math
from datetime import datetime
import scraper
from lib import get_bill_logger


def get_amount(conf):

    logger = get_bill_logger(__name__)

    id = conf["auth"]["id"]
    password = conf["auth"]["pass"]
    rent = conf["rent"]

    # 楽天カードの請求額スクレイピング
    logger.info("Calculate rakuten card billing")
    try:
        logger.info("Scrape rakuten card web")
        rakuten_bill = scraper.get_rakuten_bill(id, password)
    except Exception as e:
        raise e

    billings = []
    rakuten_bill_without_rent = math.ceil((rakuten_bill - rent["m"] - rent["f"]) / 2)
    for target in ["m", "f"]:
        total_amount = (
            rent[target] + rakuten_bill_without_rent
        )
        billing_info = {
            "rent": rent[target],
            "rakuten": rakuten_bill_without_rent,
            "total_amount": total_amount,
        }
        billings.append(billing_info)

    return billings
