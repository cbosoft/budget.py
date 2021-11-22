from budget import *

with BalanceSheet('demo.pdf', single=True) as bs:

    current = bs.add_account('Current', 300)
    savings = bs.add_account('Savings', 500)
    isa = bs.add_account('ISA', 2000)

    # Income
    bs.add_item(Income(amount=2000, when=Monthly('2nd last weekday')))

    # Savings
    bs.add_item(Transfer(amount=50, to_account=savings, when=Weekly('wednesday')))
    bs.add_item(Transfer(amount=500, to_account=isa, when=Monthly(1)))

    # Expenses/bills
    bs.add_item(Expense(name='food', amount=25, when=Weekly('sunday')))
    bs.add_item(Expense(name='rent etc', amount=500, when=Monthly(28)))
    bs.add_item(Expense(name='streaming (TV)', amount=10, when=Monthly(21)))
    bs.add_item(Expense(name='phone', amount=50, when=Monthly(16)))
    bs.add_item(Expense(name='streaming (music)', amount=10, when=Monthly(5)))

    # Misc
    bs.add_item(Expense(name='Xmas presents', amount=500, when=Once('2021-12-14')))
