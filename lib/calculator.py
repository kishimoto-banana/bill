import math
from datetime import datetime
import scraper
from lib import get_bill_logger


def _check_fullpayment(expire, current_datetime):

    is_fullpayment = False
    if (expire.strftime('%Y') == current_datetime.strftime('%Y')) and (
            expire.strftime('%m') == current_datetime.strftime('%m')):
        is_fullpayment = True

    return is_fullpayment


def _get_option_billing(options):

    options_list = []
    option_total_amount = 0
    current_datetime = datetime.now()
    for option in options:
        expire = option['expire']
        expire = datetime.strptime(expire, '%Y-%m-%d')
        if int(expire.strftime('%s')) - int(
                current_datetime.strftime('%s')) > 0:
            option_amount = math.ceil(option['amount'] / 2)
            is_fullpayment = _check_fullpayment(expire, current_datetime)
            options_list.append({
                'name': option['name'],
                'amount': option_amount,
                'is_fullpayment': is_fullpayment
            })
            option_total_amount += option_amount

    return options_list, option_total_amount


def get_amount(conf):

    logger = get_bill_logger(__name__)

    id = conf['auth']['id']
    password = conf['auth']['pass']
    rent = conf['rent']
    options = conf['options']
    fix = conf['fix']

    # 楽天カードの請求額スクレイピング
    logger.info('Calculate rakuten card billing')
    try:
        logger.info('Scrape rakuten card web')
        rakuten_bill = scraper.get_rakuten_bill(id, password)
    except Exception as e:
        raise e
    # 決定費を除く
    rakuten_bill_ex_fix = math.ceil((rakuten_bill - (fix['m'] + fix['f'])) / 2)

    logger.info('Calculate optional billing')
    options_list, option_total_amount = _get_option_billing(options)

    billings = []
    for target in ['m', 'f']:
        total_amount = rent[target] + rakuten_bill_ex_fix + fix[
            target] + option_total_amount
        billing_info = {
            'rent': rent[target],
            'rakuten': {
                "amount": rakuten_bill_ex_fix + fix[target],
                'your_only_amount': fix[target]
            },
            'options': options_list,
            'total_amount': total_amount
        }
        billings.append(billing_info)

    return billings
