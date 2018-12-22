from selenium import webdriver
import time
from lib import get_bill_logger

def get_rakuten_bill(id_, password_):

    logger = get_bill_logger(__name__)

    try:
        # headless chromeの設定
        logger.info('Setting headless chrome')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options, executable_path='driver/chromedriver')

        # トップページにアクセス
        logger.info('Get request for rakuten card')
        driver.get('https://www.rakuten-card.co.jp/')
        time.sleep(1)

        # ログイン
        logger.info('Login rakuten card')
        id = driver.find_element_by_id('u')
        id.send_keys(id_)
        password = driver.find_element_by_id('p')
        password.send_keys(password_)
        driver.find_element_by_xpath('//*[@id="indexForm"]/fieldset/button').submit()
        time.sleep(1)

        # 金額の取得
        logger.info('Extract billing')
        billing = driver.find_element_by_xpath('//*[@id="js-bill-mask"]/em').text
    
        return int(billing.replace('円', '').replace(',', ''))
    except Exception as e:   
        raise
    finally:
        # セッションの終了
        logger.info('Quit session')
        driver.quit()

    