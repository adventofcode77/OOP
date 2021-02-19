class PiggyBank:
    # create __init__ and add_money methods
    def __init__(self, dollars, cents):
        self.dollars = dollars
        self.cents = cents

    def add_money(self, deposit_dollars, deposit_cents):
        self.dollars += deposit_dollars
        self.cents += deposit_cents
        money_float = str(self.cents / 100)
        moneysplit = money_float.split('.')
        self.dollars += int(moneysplit[0])
        self.cents = int(moneysplit[1])

obj = PiggyBank(1,1)
obj.add_money(0,99)
print(obj.dollars)
