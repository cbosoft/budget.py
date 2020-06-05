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

    def __init__(self, once_on=None, starts=None, ends=None, monthly_on=0):

        assert once_on or starts or monthly_on

        self.once_on = check_convert_date(once_on)
        self.starts = check_convert_date(starts)
        self.ends = check_convert_date(ends)
        assert isinstance(monthly_on, int)
        self.monthly_on = monthly_on

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
            return date.day == self.monthly_on and in_range # TODO: what if monthly_on is 31st and month is 30 days long? or what about Feb?


        return in_range
