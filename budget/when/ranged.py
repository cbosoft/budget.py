from datetime import date

from .when import When


class Ranged(When):

    def __init__(self, start: date = None, end: date = None):
        self.start = start
        self.end = end

    def check_range(self, d: date) -> bool:
        if self.start and self.end:
            return self.start <= d <= self.end
        elif self.start:
            return self.start <= d
        elif self.end:
            return d <= self.end
        else:
            return True

    def ranged_match(self, d: date) -> bool:
        raise NotImplementedError

    def matches(self, d: date) -> bool:
        if not self.check_range(d):
            return False
        return self.ranged_match(d)
