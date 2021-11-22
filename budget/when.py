from datetime import datetime

def check_convert_date(d):

    if d is None:
        return None

    if isinstance(d, datetime):
        return d
    elif isinstance(d, str):
        return datetime.strptime(d, '%d %B %Y')
    else:
        raise Exception('date is in incorrect format (must be datetime or string of format "%d %B %Y".')

class When:

    def __init__(self, once_on=None, starts=None, ends=None, monthly_on=0, weekly_on=0):

        assert once_on or starts or monthly_on or weekly_on

        self.once_on = check_convert_date(once_on)
        self.starts = check_convert_date(starts)
        self.ends = check_convert_date(ends)
        assert isinstance(monthly_on, int)
        assert 0 <= monthly_on <= 28
        self.monthly_on = monthly_on
        assert isinstance(weekly_on, int)
        assert 0 <= weekly_on <= 4
        self.weekly_on = weekly_on

    def matches(self, date):
        
        if self.once_on:
            return date.month == self.once_on.month and date.day == self.once_on.day and date.year == self.once_on.year

        in_range = True
        if self.ends and self.starts:
            in_range = self.starts <= date <= self.ends
        elif self.ends and not self.starts:
            in_range = date <= self.ends
        elif not self.ends and self.starts:
            in_range = self.starts <= date

        if self.monthly_on:
            return date.day == self.monthly_on and in_range

        if self.weekly_on:
            return (date.day % 7) == self.weekly_on and in_range


        return in_range

    def as_monthly_change_mult(self):
        rv = 0.0

        if self.monthly_on:
            rv += 1.0

        if self.weekly_on:
            rv += 4.0

        if self.starts or self.ends:
            rv = 0

        return rv
