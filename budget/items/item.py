from datetime import datetime

from ..when import When
from ..scenario import Scenario


class Item:

    def __init__(self, *, when, name=None, annotate=False):
        assert isinstance(when, When)
        self.when = when
        self.name = name
        self.annotate = annotate

    def check(self, date: datetime) -> bool:
        return self.when.matches(date)

    def do(self, scenario: Scenario):
        raise NotImplementedError
