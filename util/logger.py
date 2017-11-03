# -*- coding: UTF-8 -*-
import logging
from logging.handlers import RotatingFileHandler
from config import LOG_PATH
import os


class Logger(object):
    def __init__(self):
        self._path = LOG_PATH

    def generate(self):
        if not os.path.isdir(os.path.dirname(LOG_PATH)):
            os.makedirs(os.path.dirname(LOG_PATH))
        log_handler = logging.getLogger('zhihu')
        log_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = RotatingFileHandler(self._path, mode='a', maxBytes=10 * 1024 * 1024, backupCount=6,
                                           encoding='utf-8')
        file_handler.setFormatter(formatter)
        log_handler.addHandler(file_handler)
        return log_handler


logger = Logger().generate()
