from typing import Union
from datetime import date

from .when import When


class Once(When):

    def __init__(self, on: Union[str, date]):
        self.on = self.check_convert_date(on)

    def matches(self, d: date):
        return d == self.on
