import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime

def _create_message(from_addr, to_addr, subject, billing):
    
    current_month = current_datetime = datetime.now().strftime('%m')
    total_amount = billing['total_amount']
    total = '{:,}'.format(total_amount)
    rent = '{:,}'.format(billing['rent'])
    rakuten = '{:,}'.format(billing['rakuten']['amount'])
     

    body = f'''{current_month}月分のソニー銀行への入金金額のお知らせです。
    
    入金金額：{total}円
    
    内訳）
    家賃：{rent}円
    楽天カード:{rakuten}円
    '''

    if billing['rakuten']['only_amount'] != 0:
        rakuten_only_amount = '{:,}'.format(billing['rakuten']['only_amount'])
        body += f'''※あなただけの支払い分が{rakuten_only_amount}円あります。
        '''
 
    for option in billing['options']:
        name = option['name']
        amount = '{:,}'.format(option['amount'])
        body += f'''{name}：{amount}円
        '''
        if option['is_fullpayment']:
            body += f'''{name}は今月で支払い完了です。
            '''

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def _send(from_addr, password, to_addrs, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(from_addr, password)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


def send_main(conf, billings):

    from_addr = conf['notification']['send']['address']
    password = conf['notification']['send']['pass']
    to_addrs = conf['notification']['receive']['address']
    subject = conf['notification']['receive']['subject']

    for idx in range(2):
        msg = _create_message(from_addr, to_addrs[idx], subject, billings[idx])
        _send(from_addr, password, to_addrs[idx], msg)