from datetime import datetime

class When:

    def __init__(self, on=None, starts=None, ends=None):

        assert on or starts

        if on:
            assert isinstance(on, datetime)
        if starts:
            assert isinstance(on, datetime)
        if ends:
            assert isinstance(on, datetime)

        self.on = on
        self.starts = starts
        self.ends = ends

    def matches(self, date):
        
        if self.on:
            return date == self.on

        if self.ends:
            return self.starts <= date <= self.ends

        return self.starts <= date
