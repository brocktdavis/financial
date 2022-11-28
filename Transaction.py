import datetime, math

class Transaction:
    
    # --FIELDS--
    # date
    # name
    # positive
    # negative
    # reimbursable
    
    def __init__(self, date, name, positive_amt, negative_amt, reimbursable=False):
        self.date = date
        self.name = name
        self.positive = positive_amt
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