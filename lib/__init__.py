from logging import getLogger, StreamHandler, FileHandler, INFO, Formatter


def get_bill_logger(modname):

    # loggerの設定
    log_file = "log/billing.log"
    log_format = Formatter("%(asctime)s [%(levelname)s] %(message)s")
    logger = getLogger(modname)
    logger.setLevel(INFO)
    logger.propagate = False
    # 標準出力へのハンドラ
    stdout_handler = StreamHandler()
    stdout_handler.setFormatter(log_format)
    logger.addHandler(stdout_handler)
    # ログファイルへのハンドラ
    file_handler = FileHandler(log_file, "a+")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger
