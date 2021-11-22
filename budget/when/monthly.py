from typing import Union, Tuple, Any
from datetime import date
from calendar import monthrange, weekday
import re

from .ranged import Ranged


class Monthly(Ranged):

    LAST_DAY_RE = re.compile(r'last (\w+)')
    NTH_DAY_RE = re.compile(r'(\d+)(?:th|nd|rd|st) day')
    NTH_DAY_FROM_END_RE = re.compile(r'(\d+)(?:th|nd|rd|st) last day')
    NTH_WEEKDAY_FROM_END_RE = re.compile(r'(\d+)(?:th|nd|rd|st) last weekday')
    ON_OR_BEFORE_RE = re.compile(r'on or before (\d+)(?:th|nd|rd|st)')

    def __init__(self, day_of_the_month: Union[str, int], start: date = None, end: date = None):
        super().__init__(start, end)
        self.spec, self.match_f = self.parse_spec(day_of_the_month)
        self.matches(date.today())

    @classmethod
    def parse_spec(cls, dom: Union[str, int]) -> Tuple[Any, callable]:
        if isinstance(dom, int):
            if dom > 28:
                raise UserWarning('day of month > 28: won\'t run every month')
            return dom, cls.match_day_num
        elif m := cls.LAST_DAY_RE.match(dom):
            dow = m.group(1)
            assert dow in cls.DAYS_OF_THE_WEEK
            dow = cls.DAYS_OF_THE_WEEK.index(dow)
            return dow, cls.match_last_day
        elif m := cls.NTH_DAY_RE.match(dom):
            dom = int(m.group(1))
            return dom, cls.match_day_num
        elif m := cls.NTH_DAY_FROM_END_RE.match(dom):
            dom = int(m.group(1))
            return dom, cls.match_last_day_num
        elif m := cls.NTH_WEEKDAY_FROM_END_RE.match(dom):
            dom = int(m.group(1))
            return dom, cls.match_last_weekday_num
        else:
            raise NotImplementedError(f'"{dom}"')

    def ranged_match(self, d: date):
        return self.match_f(self.spec, d)

    @staticmethod
    def match_day_num(day_num: int, d: date):
        return day_num == d.day

    @staticmethod
    def match_last_day_num(day_num: int, d: date):
        _, lom = monthrange(d.year, d.month)
        return (lom - day_num) == d.day

    @staticmethod
    def match_last_weekday_num(day_num: int, d: date):
        _, lom = monthrange(d.year, d.month)
        target_day = lom - day_num
        target_dow = weekday(d.year, d.month, target_day)
        while target_dow > 4:
            target_day -= 1
            target_dow = weekday(d.year, d.month, target_day)
        return target_day == d.day

    @staticmethod
    def match_last_day(day_of_week_num: int, d: date):
        _, lom = monthrange(d.year, d.month)
        this_dow = weekday(d.year, d.month, d.day)
        return (day_of_week_num == this_dow) and (lom - day_of_week_num <= 7)

    @staticmethod
    def match_on_or_before(dom: int, d: date):
        _, lom = monthrange(d.year, d.month)
        target_day = min(dom, lom)
        return target_day == d.day
