from typing import List, Dict
from datetime import datetime, timedelta

from .scenario import Scenario


class FinanceSim:

    def __init__(self):
        self.t = datetime.today()
        self.delta_t = timedelta(days=1)

    def timestep(self, scenario: Scenario, data: Dict[str, List[float]]):
        for item in scenario.items:
            if item.check(self.t):
                item.do(scenario)
        for n, acc in scenario.accounts_by_name.items():
            data[n].append(acc.value)
        self.t += self.delta_t

    def run(self, scenario: Scenario, start_or_end: datetime, end: datetime = None):
        if end:
            self.t = start_or_end
        else:
            end = start_or_end
        data = {n: list() for n in scenario.accounts_by_name}
        while self.t < end:
            self.timestep(scenario, data)
        return data
