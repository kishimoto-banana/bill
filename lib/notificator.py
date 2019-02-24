import requests
import json
from datetime import datetime
from lib import get_bill_logger

def _create_message_common():
    
    current_month = current_datetime = datetime.now().strftime('%m')
    text = f'''
    {current_month}月分のソニー銀行への入金金額のお知らせだよ。
    26日までに入金してね。
    '''

    return text

def _create_message(billing, name):
    
    total_amount = billing['total_amount']
    total = '{:,}'.format(total_amount)
    rent = '{:,}'.format(billing['rent'])
    rakuten = '{:,}'.format(billing['rakuten']['amount'])
     

    body = f'''
    <{name}>
    入金金額：{total}円
    
    内訳）
    家賃：{rent}円
    楽天カード:{rakuten}円
    '''

    if billing['rakuten']['only_amount'] != 0:
        rakuten_only_amount = '{:,}'.format(billing['rakuten']['only_amount'])
        body += f'''
        ※あなただけの支払い分が{rakuten_only_amount}円あるよ。
        '''
 
    for option in billing['options']:
        name = option['name']
        amount = '{:,}'.format(option['amount'])
        body += f'''{name}：{amount}円
        '''
        if option['is_fullpayment']:
            body += f'''{name}は今月で支払い完了だよー。
            '''

    return body

def _post_slack(post_url, name, text, icon):

    requests.post(
        post_url,
        data=json.dumps(
            {"text": text,
             "username": name,
             "icon_emoji": icon,
             'link_names': 1}))


def send_main(conf, billings):

    logger = get_bill_logger(__name__)
    post_url = conf['notification']['post_url']
    appname = conf['notification']['appname']
    icon_emoji = conf['notification']['icon_emoji']
    names = conf['notification']['name']

    logger.info(f'Create message for common')
    msg = _create_message_common()
    logger.info(f'Send message for common')
    _post_slack(post_url, appname, msg, icon_emoji)

    for idx in range(2):
        logger.info(f'Create message for {idx}')
        msg = _create_message(billings[idx], names[idx])
        logger.info(f'Send message for {idx}')
        _post_slack(post_url, appname, msg, icon_emoji)