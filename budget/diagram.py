from datetime import datetime, timedelta

class Diagram:

    def __init__(self):
        self.params = dict()

    def set_params(self, **kwargs):
        self.params = {**self.params, **kwargs}

    def get_time_extents(self, start=None, end=None, **kwargs):

        today = datetime.today()

        if not start or isinstance(start, int):
            n_months = 0
            if isinstance(start, int):
                assert start < 0
                n_months = start
            start = today + timedelta(days=n_months*31)

        if not end or isinstance(end, int):
            n_months = 6
            if isinstance(end, int):
                assert end > 0
                n_months = end
            end = today + timedelta(days=n_months*31)

        return start, end

    def plot(self):
        raise NotImplementedError("Defined in sub class; don't use Diagram obj directly")
