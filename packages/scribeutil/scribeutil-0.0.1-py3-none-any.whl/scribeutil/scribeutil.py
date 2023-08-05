# Python's Libraries
import re
import logging

# Own's Libraries
from errors import InvalidValueError

loggers = {}


class ScribeUtil(object):

    @classmethod
    def get_Logger(self, _logger_name, _with_time=False):
        if loggers.get(_logger_name):
            return loggers.get(_logger_name)

        else:
            level = logging.INFO

            if _with_time:
                str_format = '[%(levelname)s] %(asctime)s: %(message)s'

            else:
                str_format = '[%(levelname)s] %(message)s'

            logging.root.handlers = []
            logging.basicConfig(
                format=str_format,
                level=level,
                datefmt='%d-%b-%y %H:%M:%S'
            )

            logger = logging.getLogger(_logger_name)
            loggers[_logger_name] = logger

            return logger

    @classmethod
    def validate_Email(self, _value):
        """This function validate if a value provided is valid email

        :param _value: value to be validated
        :type _value: str
        :raises InvalidValueError: If the value provide is not a valid email
        """

        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        if re.fullmatch(regex, _value) is None:
            raise InvalidValueError(
                f"{_value} is not a email value valid",
                _error="INVALID_EMAIL"
            )


# MSGS LEVELS:
# - CRITICAL    50
# - ERROR   40
# - WARNING 30
# - INFO    20
# - DEBUG   10
# - NOTSET  0
