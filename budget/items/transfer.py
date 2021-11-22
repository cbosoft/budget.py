from typing import Union

from .item import Item, Scenario, When
from ..account import Account


class Transfer(Item):

    def __init__(self, *, amount: float, from_account: Union[str, int, Account], to_account: Union[str, int, Account],
                 when: When, **kwargs):
        super().__init__(when=when, **kwargs)
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account

    @staticmethod
    def get_account(scenario: Scenario, idx_name_or_value: Union[str, int, Account]):
        if isinstance(idx_name_or_value, str):
            return scenario.accounts_by_name[idx_name_or_value]
        elif isinstance(idx_name_or_value, int):
            return scenario.accounts[idx_name_or_value]
        else:
            assert isinstance(idx_name_or_value, Account)
            return idx_name_or_value

    def do(self, scenario: Scenario):
        f_acc: Account = self.get_account(scenario, self.from_account)
        t_acc: Account = self.get_account(scenario, self.to_account)
        f_acc.withdraw_funds(self.amount)
        t_acc.add_funds(self.amount)
