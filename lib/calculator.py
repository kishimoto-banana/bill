import scraper
from datetime import datetime
import math

def _check_fullpayment(expire, current_datetime):

    is_fullpayment = False
    if (expire.strftime('%Y') == current_datetime.strftime('%Y')) and (expire.strftime('%m') == current_datetime.strftime('%m')):
        is_fullpayment = True

    return is_fullpayment

def get_amount(conf):

    id = conf['auth']['id']
    password = conf['auth']['pass']
    rent = conf['rent']
    options = conf['options']
    fix = conf['fix']

    # 請求情報の辞書
    billing = {}

    # 家賃
    rent = math.ceil(rent / 2)
    total_amount = rent
    billing.update({'rent':rent})

    # 変動費
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
    try:
        rakuten_bill = scraper.get_rakuten_bill(id, password)
        rakuten_bill = math.ceil(rakuten_bill / 2)
        total_amount += rakuten_bill
        billing.update({'rakuten':rakuten_bill})
    except Exception as e:
        raise

    billing.update({'total_amount':total_amount})
    return billing