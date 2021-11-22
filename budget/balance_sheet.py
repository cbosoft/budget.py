from typing import Dict
from datetime import datetime, timedelta
import re

from matplotlib import pyplot as plt

from .items import Item
from .scenario import Scenario
from .sim import FinanceSim
from .account import Account


class BalanceSheet:

    def __init__(self, name, *accounts: Account):
        self.name = name
        self.accounts = list(accounts)
        self.scenarios: Dict[str, Scenario] = {}
        self.start = datetime.today()
        self.end = datetime.today()+timedelta(weeks=6*4)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.plot()

    def add_account(self, name: str, balance=0.0):
        self.accounts.append(Account(name=name, current_value=balance))

    def add_item(self, item, scenario='default'):
        if scenario not in self.scenarios:
            self.scenarios[scenario] = Scenario(*self.accounts, name=scenario)
        self.scenarios[scenario].add_item(item)

    def add_item_to_matching_scenarios(self, pattern, *args, **kwargs):
        item = Item(*args, **kwargs)
        pattern_re = re.compile(pattern)
        for name, scenario in self.scenarios.items():
            if pattern_re.match(name):
                scenario.add_item(item)

    def plot(self):
        sim = FinanceSim()
        n = len(self.accounts)
        fig, axes = plt.subplots(nrows=len(self.accounts), sharex='col', figsize=(7, 4*n))
        for ax, acc in zip(axes, self.accounts):
            plt.sca(ax)
            plt.title(acc.name)
        for sce_n, scenario in self.scenarios.items():
            data = sim.run(scenario, self.start, self.end)
            for i, (acc_n, v) in enumerate(data.items()):
                plt.sca(axes[i])
                plt.plot(v, label=sce_n)
        plt.tight_layout()
        plt.show()
