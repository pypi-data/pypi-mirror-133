
# Python's Libraries
import re

# Own's Libraries
from .errors import InvalidValueError


class DataTool(object):

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
