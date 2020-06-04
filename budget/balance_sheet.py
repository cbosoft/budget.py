from datetime import datetime, timedelta

from budget.item import Item

def iter_dates(start, end):
    for i in range( (end-start).days ):
        yield start + timedelta(days=i)

class BalanceSheet:

    def __init__(self, initial_value=0.0):
        self.initial_value = initial_value
        self.items = []

    def add_item(self, *args, **kwargs):
        self.items.append(Item(*args, **kwargs))

    def plot(self, start=None, end=None):

        today = datetime.today()

        if not start:
            start = today - timedelta(days=31)

        if not end:
            end = today + timedelta(days=6*31)

        balance = self.initial_value
        for date in iter_dates(start, end):
            for item in self.items:
                # returns 0.0 if not a matching date
                balance += item.check(date)
        print(balance)
