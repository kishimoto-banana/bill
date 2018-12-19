from selenium import webdriver
import time

def get_rakuten_bill(id_, password_):

    try:
        # headless chromeの設定
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options, executable_path='driver/chromedriver')

        # トップページにアクセス
        driver.get('https://www.rakuten-card.co.jp/')
        time.sleep(1)

        # ログイン
        id = driver.find_element_by_id('u')
        id.send_keys(id_)
        password = driver.find_element_by_id('p')
        password.send_keys(password_)
        driver.find_element_by_xpath('//*[@id="indexForm"]/fieldset/button').submit()
        time.sleep(1)

        # 金額の取得
        billing = driver.find_element_by_xpath('//*[@id="js-bill-mask"]/em').text

        return int(billing.replace('円', '').replace(',', ''))
    except Exception as e:   
        raise
    finally:
        # セッションの終了
        driver.quit()

    