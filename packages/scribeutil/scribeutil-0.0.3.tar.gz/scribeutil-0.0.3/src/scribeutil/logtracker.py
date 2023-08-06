# Python's Libraries
import logging


loggers = {}


class LogTracker(object):

    @classmethod
    def get_Logger(self, _logger_name, _with_time=True):
        if loggers.get(_logger_name):
            return loggers.get(_logger_name)

        else:
            level = logging.INFO

            if _with_time:
                str_format = '[%(levelname)s] %(asctime)s: %(message)s'

            else:
                str_format = '[%(levelname)s]: %(message)s'

            logging.root.handlers = []
            logging.basicConfig(
                format=str_format,
                level=level,
                datefmt='%d-%b-%y %H:%M:%S'
            )

            logger = logging.getLogger(_logger_name)
            loggers[_logger_name] = logger

            return logger

# MSGS LEVELS:
# - CRITICAL    50
# - ERROR   40
# - WARNING 30
# - INFO    20
# - DEBUG   10
# - NOTSET  0
