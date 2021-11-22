from typing import Union

from datetime import date, datetime


class When:

    DAYS_OF_THE_WEEK = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

    def matches(self, d: date) -> bool:
        raise NotImplementedError

    @staticmethod
    def check_convert_date(d: Union[date, str]) -> date:
        if isinstance(d, date):
            return d
        elif isinstance(d, str):
            return datetime.strptime(d, '%Y-%m-%d').date()
        else:
            raise ValueError('date is in incorrect format (must be datetime or string of format "YYYY-MM-DD".')
