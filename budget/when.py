from datetime import datetime

class When:

    def __init__(self, once_on=None, starts=None, ends=None, monthly_on=None):

        assert once_on or starts or monthly_on

        if once_on:
            assert isinstance(once_on, datetime)
        if starts:
            assert isinstance(starts, datetime)
        if ends:
            assert isinstance(ends, datetime)
        if monthly_on:
            assert isinstance(monthly_on, int)

        self.once_on = once_on
        self.starts = starts
        self.ends = ends
        self.monthly_on = monthly_on

    def matches(self, date):
        
        if self.once_on:
            return date == self.once_on

        in_range = True
        if self.ends and self.starts:
            in_range = self.starts <= date <= self.ends
        elif self.ends and not self.starts:
            in_range = date <= self.ends
        elif not self.ends and self.starts:
            in_range = self.starts <= date

        if self.monthly_on:
            return date.day == self.monthly_on and in_range # TODO: what if monthly_on is 31st and month is 30 days long? or what about Feb?


        return in_range
