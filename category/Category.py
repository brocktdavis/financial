class Category:
    
    def __init__(self, name, children):
        self.name = name
        self.transactions = []
        self.children = children if children is not None else []
    
    def __str__(self, spacing=""):
        ret = spacing + self.name + "\n"
        for c in self.children:
            ret += c.__str__(spacing + "  ")
        return ret
    
    def _isLeaf(self):
        return len(self.children) == 0
    
