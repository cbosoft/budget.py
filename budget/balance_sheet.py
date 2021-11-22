from typing import Dict
from datetime import date, timedelta
import re

from matplotlib import pyplot as plt
import numpy as np

from .items import Item
from .scenario import Scenario
from .sim import FinanceSim
from .account import Account


class BalanceSheet:

    def __init__(self, name, *accounts: Account, single=False, currency='£'):
        self.name = name
        self.single = single
        self.accounts = list(accounts)
        self.scenarios: Dict[str, Scenario] = {}
        self.start = date.today()
        self.end = date.today()+timedelta(days=365//2)
        self.currency = currency

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.plot()

    def add_account(self, name: str, balance=0.0) -> str:
        self.accounts.append(Account(name=name, current_value=balance))
        return name

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
        w, h = 7, 4
        if self.single:
            fig = plt.figure(figsize=(w, h))
            ax = plt.gca()
            axes = [ax]*n
        else:
            fig, axes = plt.subplots(nrows=len(self.accounts), sharex='col', figsize=(w, h*n))
            for ax, acc in zip(axes, self.accounts):
                plt.sca(ax)
                plt.title(acc.name)

        data = dict()
        totals = 0
        for sce_n, scenario in self.scenarios.items():
            data = sim.run(scenario, self.start, self.end)
            for i, (acc_n, v) in enumerate(data['daily_data'].items()):
                plt.sca(axes[i])
                plt.plot(v, label=acc_n if self.single else sce_n)
                totals = np.add(v, totals)
            monthly_change = np.diff(data['monthly_data']['Current'])
            median_change = np.median(monthly_change)
            pm = '+' if median_change > 0 else '-'
            change_str = f'Median monthly change {pm}{self.currency}{median_change:.2f}'
            if self.single:
                plt.title(change_str)
            else:
                print(change_str)
        # ax = plt.gca()
        # plt.twinx()
        # plt.plot(totals, color='k', label='total')
        # plt.ylabel('Total £')
        # locs, _ = plt.yticks()
        # plt.yticks(locs, [f'{int(l//1000)}k' for l in locs])
        # plt.sca(ax)
        print(f'Total {self.currency}{totals[-1]:.2f}')
        month_ticks = data['month_ind']
        plt.xticks(*zip(*month_ticks))
        locs, _ = plt.yticks()
        plt.yticks(locs, [f'{int(l//1000)}k' for l in locs])
        plt.axhline(0, color='0.8')
        plt.ylabel(f'Balance [{self.currency}]')
        plt.legend(loc='upper left')
        plt.tight_layout()
        if self.name:
            plt.savefig(self.name)
        else:
            plt.show()
