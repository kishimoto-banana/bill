import scraper
from datetime import datetime
import math
from lib import get_bill_logger

def _check_fullpayment(expire, current_datetime):

    is_fullpayment = False
    if (expire.strftime('%Y') == current_datetime.strftime('%Y')) and (expire.strftime('%m') == current_datetime.strftime('%m')):
        is_fullpayment = True

    return is_fullpayment

def get_amount(conf):

    logger = get_bill_logger(__name__)

    id = conf['auth']['id']
    password = conf['auth']['pass']
    rent = conf['rent']
    options = conf['options']
    fix = conf['fix']

    # 請求情報の辞書
    billing = {}

    # 家賃
    logger.info('Calculate rent')
    rent = math.ceil(rent / 2)
    total_amount = rent
    billing.update({'rent':rent})

    # 変動費
    logger.info('Calculate optional billing')
    options_list = []
    current_datetime = datetime.now()
    for option in options:
        expire = option['expire']
        expire = datetime.strptime(expire, '%Y-%m-%d')
        if int(expire.strftime('%s')) - int(current_datetime.strftime('%s')) > 0:
            amount = math.ceil(option['amount'] / 2)
            total_amount += amount
            is_fullpayment = _check_fullpayment(expire, current_datetime)
            options_list.append({'name':option['name'], 'amount':amount, 'is_fullpayment':is_fullpayment})
    billing.update({'options':options_list})

    # 楽天カード
    logger.info('Calculate rakuten card billing')
    billings = []
    try:
        logger.info('Scrape rakuten card web')
        rakuten_bill = scraper.get_rakuten_bill(id, password)

        # 決定費を除く
        fix_amount = fix['0'] + fix['1']
        rakuten_bill = math.ceil((rakuten_bill - fix_amount) / 2)
        total_amount += rakuten_bill

        for idx in range(2):
            billing_copy = billing.copy()
            billing_copy.update({'rakuten':{"amount":rakuten_bill + fix[str(idx)], 'only_amount':fix[str(idx)]}, 'total_amount':total_amount + fix[str(idx)]})
            billings.append(billing_copy)

    except Exception as e:
        raise

    return billings