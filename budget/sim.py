from typing import List, Dict
from datetime import date, timedelta
from calendar import monthrange, month_name

from .scenario import Scenario


class FinanceSim:

    def __init__(self):
        self.t = date.today()
        self.delta_t = timedelta(days=1)

    def timestep(self, scenario: Scenario, data: Dict[str, List[float]]):
        for item in scenario.items:
            if item.check(self.t):
                item.do(scenario)
        for n, acc in scenario.accounts_by_name.items():
            data[n].append(acc.value)
        self.t += self.delta_t

    def run(self, scenario: Scenario, start: date, end: date):
        self.t = start
        daily_data = {n: list() for n in scenario.accounts_by_name}
        monthly_data = {n: list() for n in scenario.accounts_by_name}
        step = 1
        month_ind = []
        while self.t < end:
            self.timestep(scenario, daily_data)
            step += 1
            if self.is_start_of_month():
                for n, acc in scenario.accounts_by_name.items():
                    monthly_data[n].append(acc.value)
            if self.is_middle_of_month():
                month_ind.append((step, month_name[self.t.month]))
        return dict(
            daily_data=daily_data,
            monthly_data=monthly_data,
            month_ind=month_ind)

    def is_end_of_month(self) -> bool:
        _, lom = monthrange(self.t.year, self.t.month)
        return self.t.day == lom

    def is_start_of_month(self) -> bool:
        return self.t.day == 1

    def is_middle_of_month(self) -> bool:
        return self.t.day == 14
