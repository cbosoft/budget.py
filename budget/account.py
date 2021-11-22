class Account:

    def __init__(self, name: str, current_value=0.0):
        self.name = name
        self.value = current_value

    def withdraw_funds(self, amount):
        self.value -= amount

    def add_funds(self, amount):
        self.value += amount

