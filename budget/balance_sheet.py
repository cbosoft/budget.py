from datetime import datetime, timedelta

from matplotlib import pyplot as plt

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
        plt.axhline(0, color='0.5', ls='--')


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




    def get_delta_items(self, date):
        delta = 0.0
        for item in self.items:
            delta += item.check(date)
        return delta


    def get_delta_scenario(self, date, scenario):
        assert isinstance(scenario, (str, list))

        if isinstance(scenario, list):
            return sum([self.get_delta_scenario(date, s) for s in scenario])

        assert scenario in self.scenarios

        delta = 0.0
        for item in self.scenarios[scenario].items:
            delta += item.check(date)

        return delta



    def plot(self, start=None, end=None, with_scenario=False, month_every=1):

        today = datetime.today()

        if not start or isinstance(start, int):
            n_months = -1
            if isinstance(start, int):
                assert start < 0
                n_months = start
            start = today + timedelta(days=n_months*31)

        if not end or isinstance(end, int):
            n_months = 6
            if isinstance(end, int):
                assert end > 0
                n_months = end
            end = today + timedelta(days=n_months*31)

        xtick_labels = list()
        xtick_locs = list()
        days = list()
        balance = list()
        for i, date in enumerate(iter_dates(start, end)):
            days.append(i)
            if date.day == 1 and date.month % month_every == 0:
                xtick_labels.append(date.strftime('%B'))
                xtick_locs.append(i)

            delta = self.get_delta_items(date)

            if with_scenario:
                delta += self.get_delta_scenario(date, with_scenario)

            if balance:
                balance.append(balance[-1] + delta)
            else:
                balance.append(self.initial_value + delta)

        # Add a point at zero so that bottom ylim is at minimum zero
        days.insert(0, 0)
        balance.insert(0, 0)
        days.insert(1, float('nan'))
        balance.insert(1, float('nan'))
        plt.plot(days, balance, label='default' if not with_scenario else with_scenario)
        plt.xticks(xtick_locs, xtick_labels, rotation=90)
