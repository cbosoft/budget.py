from typing import Union

from .item import Item, Scenario, When
from ..account import Account


class Expense(Item):

    def __init__(self, *, amount: float, account: Union[str, int] = 0, when: When, **kwargs):
        super().__init__(when=when, **kwargs)
        self.amount = amount
        self.account = account

    def do(self, scenario: Scenario):
        acc: Account
        if isinstance(self.account, str):
            acc = scenario.accounts_by_name[self.account]
        else:
            acc = scenario.accounts[self.account]
        acc.withdraw_funds(self.amount)
