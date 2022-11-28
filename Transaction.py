import datetime, math

class Transaction:
    
    # --FIELDS--
    # date: A datetime object describing when the transaction took place
    # name: A name for the transaction, usually a vendor's description
    # positive: The positive amount associated with this transaction (a positive number itself)
    # negative: The negative amount associated with this transaction (a positive number itself)
    # reimbursable: True if the transaction is reimbursable
    
    def __init__(self, date, name, positive_amt, negative_amt, reimbursable=False):
        self.date = date
        self.name = name
        if positive_amt < 0:
            raise ValueError("Positive amount should be non-negative")
        self.positive = positive_amt
        if negative_amt < 0:
            raise ValueError("Negative amount should be non-negative")
        self.negative = negative_amt
        self.reimbursable = reimbursable
    
    def __str__(self):
        string = "(" + str(self.date) + ") "
        # Dollar amt
        string += str(self.amount())
        # Name
        return string + " " + self.name + (" R" if self.reimbursable else "")
    def __repr__(self): return self.__str__()
    
    def amount(self): return self.income() - self.expense()
    def income(self): return 0 if math.isnan(self.positive) else self.positive
    def expense(self): return 0 if math.isnan(self.negative) else self.negative

if __name__ == '__main__':
    print('Transaction Class')
    t = Transaction(datetime.now, 'Transaction A', 100, 0, True)