from datetime import datetime, timedelta

from budget.item import Item
from budget.scenario import Scenario

def iter_dates(start, end):
    for i in range( (end-start).days ):
        yield start + timedelta(days=i)

class BalanceSheet:

    def __init__(self, initial_value=0.0):
        self.initial_value = initial_value
        self.items = []
        self.scenarios = {}

    def add_item(self, *args, **kwargs):
        self.items.append(Item(*args, **kwargs))


    def add_item_to_scenario(self, scenario, *args, **kwargs):
        if scenario not in self.scenarios:
            self.scenarios[scenario] = Scenario()
        self.scenarios[scenario].items.append(Item(*args, **kwargs))


    def plot_scenarios(self, *args, **kwargs):
        self.plot(*args, **kwargs)
        for scenario in self.scenarios.keys():
            self.plot(*args, with_scenario=scenario, **kwargs)


    def plot(self, start=None, end=None, with_scenario=False, month_every=3):

        today = datetime.today()

        if not start:
            start = today - timedelta(days=31)

        if not end:
            end = today + timedelta(days=6*31)

        balance = self.initial_value
        for date in iter_dates(start, end):
            delta = 0.0
            for item in self.items:
                delta += item.check(date)

            if with_scenario:
                for item in self.scenarios[with_scenario].items:
                    delta += item.check(date)

            if balance:
                balance.append(balance[-1] + delta)
            else:
                balance.append(self.initial_value + delta)
