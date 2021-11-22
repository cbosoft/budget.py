from datetime import datetime, timedelta
import re

from matplotlib import pyplot as plt

from budget.item import Item
from budget.scenario import Scenario, all_possible_combinations_of
from budget.diagram import Diagram
from budget.util import iter_dates


class BalanceSheet(Diagram):

    def __init__(self, initial_value=0.0):
        super().__init__()
        self.initial_value = initial_value
        self.items = []
        self.scenarios = {}
        plt.axhline(0, color='0.5', ls='--')
        self.params = dict(
                scenarios=False,
                combine_scenarios=False,
                ends=None,
                starts=None,
                month_every=1)

    def add_item(self, scenario=None, **kwargs):
        if scenario is not None:
            self.add_item_to_scenario(scenario, **kwargs)
        else:
            self.items.append(Item(**kwargs))

    def add_item_to_scenario(self, scenario, **kwargs):
        if scenario not in self.scenarios:
            self.scenarios[scenario] = Scenario()
            self.params['scenarios'] = True
        self.scenarios[scenario].items.append(Item(**kwargs))

    def add_item_to_matching_scenarios(self, pattern, *args, **kwargs):
        item = Item(*args, **kwargs)
        pattern_re = re.compile(pattern)
        for name, scenario in self.scenarios.items():
            if pattern_re.match(name):
                scenario.items.append(item)

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


    def plot(self):
        if self.params['scenarios']:
            if self.params['combine_scenarios']:
                self._plot_combine_scenarios(**self.params)
            else:
                self._plot_scenarios(**self.params)
        else:
            self._plot(**self.params)
        plt.plot([0], [0])
        plt.legend(loc='center left', bbox_to_anchor=(1.01, 0.5))
        plt.axhline(0.0, color='red')


    def _plot_scenarios(self, *args, **kwargs):
        self._plot(*args, **kwargs)
        for scenario in self.scenarios.keys():
            self._plot(*args, with_scenario=scenario, **kwargs)


    def _plot_combine_scenarios(self, *args, **kwargs):
        self._plot(*args, **kwargs)
        # combine all scenarios
        scenario_list = list(self.scenarios.keys())
        for scenario_combo in all_possible_combinations_of(scenario_list):
            self._plot(*args, with_scenario=scenario_combo, **kwargs)


    def _plot(self, with_scenario=False, month_every=1, **kwargs):

        start, end = self.get_time_extents(**kwargs)

        xtick_labels = list()
        xtick_locs = list()
        days = list()
        balance = list()
        pyear = start.year
        for i, date in enumerate(iter_dates(start, end)):
            if date.year != pyear:
                plt.axvline(i, color='0.5', lw=1)
                pyear = date.year
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

        if isinstance(with_scenario, list):
            if len(with_scenario) == 1:
                with_scenario = with_scenario[0]
            else:
                with_scenario = ', '.join(with_scenario[:-1]) + ' and ' + with_scenario[-1]

        # Add a point at zero so that bottom ylim is at minimum zero
        days.insert(0, 0)
        balance.insert(0, 0)
        days.insert(1, float('nan'))
        balance.insert(1, float('nan'))
        plt.plot(days, balance, label='default' if not with_scenario else with_scenario)
        plt.xticks(xtick_locs, xtick_labels, rotation=90)
