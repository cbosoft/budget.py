from typing import Dict, List

from .account import Account


class Scenario:

    def __init__(self, *accounts: Account, name=None):
        self.accounts = accounts
        self.accounts_by_name: Dict[str, Account] = {account.name: account for account in self.accounts}
        self.name = name
        self.items: List["Item"] = []

    def add_item(self, item):
        self.items.append(item)


def _next_level_combo(last, scenarios):
    rv = list()
    for s in scenarios:
        for l in last:
            if s in l or s == l:
                continue

            if isinstance(l, list):
                n = list(sorted([*l,s]))
            else:
                n = list(sorted([l, s]))

            if n not in rv:
                rv.append(n)
    return rv


def all_possible_combinations_of(scenarios):
    combinations = [list(scenarios)]
    for i in range(len(scenarios)-1):
        combinations.append(_next_level_combo(combinations[-1], scenarios))
    rv = list()
    for comb in combinations:
        rv.extend(comb)
    return rv
