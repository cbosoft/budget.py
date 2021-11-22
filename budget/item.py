from budget.when import When


class Item:

    def __init__(self, *, amount, when, name=None, annotate=False):
        assert isinstance(amount, (float, int))
        self.amount = amount

        assert isinstance(when, When)
        self.when = when

        self.name = name
        self.annotate = annotate

    def check(self, date):
        if self.when.matches(date):
            return self.amount
        return 0.0

    def as_monthly_change(self):
        return self.amount*self.when.as_monthly_change_mult()
