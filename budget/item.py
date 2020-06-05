from budget.when import When

class Item:

    def __init__(self, amount, when, name=None):
        assert isinstance(amount, (float, int))
        self.amount = amount

        assert isinstance(when, When)
        self.when = when

    def check(self, date):
        if self.when.matches(date):
            return self.amount
        return 0.0
