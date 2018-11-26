from datetime import datetime
import logging
import os


def get_logger(name):
    log_file_name = "logfile_" + datetime.now().strftime("%d_%m_%Y.txt")
    log_directory = os.path.join("../logs", log_file_name)

    file_handler = logging.FileHandler(log_directory, 'a')
    file_formatter = logging.Formatter('**%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
    file_handler.setFormatter(file_formatter)

    logger = logging.getLogger(name)
    logger.handlers = []

    logger.addHandler(file_handler)
    return logger
