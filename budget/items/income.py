from .expense import Expense, Scenario
from ..account import Account


class Income(Expense):

    def do(self, scenario: Scenario):
        acc: Account
        if isinstance(self.account, str):
            acc = scenario.accounts_by_name[self.account]
        else:
            acc = scenario.accounts[self.account]
        acc.add_funds(self.amount)
