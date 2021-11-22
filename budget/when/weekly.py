from datetime import date

from .ranged import Ranged


class Weekly(Ranged):

    DAYS_OF_THE_WEEK = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

    def __init__(self, day_of_week: str, start: date = None, end: date = None):
        super().__init__(start, end)
        assert day_of_week in self.DAYS_OF_THE_WEEK
        self.dow = self.DAYS_OF_THE_WEEK.index(day_of_week)

    def ranged_match(self, d: date):
        return self.dow == (d.isoweekday() - 1)
