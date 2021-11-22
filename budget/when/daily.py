from datetime import date

from .ranged import Ranged


class Daily(Ranged):

    def ranged_match(self, d: date) -> bool:
        return True
