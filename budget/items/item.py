from datetime import date

from ..when.when import When
from ..scenario import Scenario


class Item:

    def __init__(self, *, when, name=None, annotate=False):
        assert isinstance(when, When)
        self.when = when
        self.name = name
        self.annotate = annotate

    def check(self, d: date) -> bool:
        return self.when.matches(d)

    def do(self, scenario: Scenario):
        raise NotImplementedError
