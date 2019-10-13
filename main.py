import os
import sys
import json

# ルートディレクトリをアプリケーションのホーム(${app_home})に設定
app_home = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# ${app_home}/libをライブラリロードパスに追加
sys.path.append(os.path.join(app_home, 'lib'))

import calculator
import notificator
from lib import get_bill_logger


def main():

    # 設定ファイル
    config_path = 'conf/settings.json'
    with open(config_path) as f:
        conf = json.load(f)

    # loggerの設定
    logger = get_bill_logger(__name__)

    try:
        logger.info('Start Calculating billing')
        billings = calculator.get_amount(conf)
        logger.info(billings)
        logger.info('Start notification')
        # notificator.send_main(conf, billings)
        logger.info('Success')
    except Exception as e:
        logger.exception(f'{e}')
        exit(1)


if __name__ == '__main__':
    main()
