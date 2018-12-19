import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime

def _create_message(from_addr, to_addrs, subject, billing):
    
    current_month = current_datetime = datetime.now().strftime('%m')
    total_amount = billing['total_amount']
    total = '{:,}'.format(int(total_amount / 2))
    rent = '{:,}'.format(int(billing['rent'] / 2))
    rakuten = '{:,}'.format(int(billing['rakuten'] / 2))

    body = f'''{current_month}月分のソニー銀行への入金金額のお知らせです。
    
    入金金額：{total}円
    
    内訳）
    家賃：{rent}円
    楽天カード:{rakuten}円
    '''

    for option in billing['options']:
        name = option['name']
        amount = '{:,}'.format(int(option['amount'] / 2))
        body += f'''{name}：{amount}円
        '''
        if option['is_fullpayment']:
            body += f'''{name}は今月で支払い完了です。
            '''

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ",".join(to_addrs)
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


def send_main(conf, billing):

    from_addr = conf['notification']['send']['address']
    password = conf['notification']['send']['pass']
    to_addrs = conf['notification']['receive']['address']
    subject = conf['notification']['receive']['subject']

    msg = _create_message(from_addr, to_addrs, subject, billing)
    _send(from_addr, password, to_addrs, msg)