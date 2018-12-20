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
# TODO: どっちかの負担が確定している場合

def main():

    # 設定ファイル
    conifg_path = 'conf/settings.json'
    with open(conifg_path) as f:
        conf = json.load(f)
    
    try:
        billing = calculator.get_amount(conf)
        print(billing)
        notificator.send_main(conf, billing)
    except Exception as e:
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    main()