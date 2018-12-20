import os
import sys
import json
import traceback

# ルートディレクトリをアプリケーションのホーム(${app_home})に設定
app_home = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# ${app_home}/libをライブラリロードパスに追加
sys.path.append(os.path.join(app_home, 'lib'))

import calculator
import notificator

# TODO: logger

def main():

    # 設定ファイル
    conifg_path = 'conf/settings.json'
    with open(conifg_path) as f:
        conf = json.load(f)
    
    try:
        billings = calculator.get_amount(conf)
        print(billings)
        notificator.send_main(conf, billings)
    except Exception as e:
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    main()