import json, pickledb
from easygui import *

def load():
    with open('category/categories.json', 'r') as f:
        categories = json.load(f)
    return Categories([Category(obj) for obj in categories])

# Internal DFS for finding category
def _findCat(categories, name):
    for c in categories:
        if c.name == name:
            return c
        childCat = _findCat(c.children, name)
        if childCat: return childCat
    return None

class Category:
    def __init__(self, obj):
        self.name = obj['name']
        self.children = [Category(o) for o in obj['children']] if 'children' in obj else []
        self.transactions = []
    
    def __str__(self):
        return "%s [%d] $%d" % (self.name, len(self.transactions), self.singleAmount())
    
    def __repr__(self, spacing=""):
        ret = spacing + self.__str__() + '\n'
        for c in self.children:
            ret += c.__repr__(spacing + '  ')
        return ret
    
    def addTransaction(self, t):
        self.transactions.append(t)
    
    def singleAmount(self):
        return sum([t.amount() for t in self.transactions])
    
    def totalAmount(self):
        return self.singleAmount + sum([c.totalAmount for c in self.children])
    
class Categories:
    def __init__(self, topLevelCategories):
        self.topLevelCategories = topLevelCategories
        self.db = pickledb.load('category/mappings.db', False)
    
    def __str__(self): return '\n'.join([repr(cat).strip() for cat in self.topLevelCategories])
    def __repr__(self): return self.__str__()
    
    def addTransaction(self, t):
        # If already have mapping, add directly to category
        if self.db.exists(t.name):
            self.findCategory(self.db.get(t.name)).addTransaction(t)
            return True
        
        # Present user input and add mapping
        choice = self._presentCategoryChoice(t)
        if choice:
            self.findCategory(choice).addTransaction(t)
            self.db.set(t.name, choice)
            return True
        
        # If user canceled, flush to DB store
        self.db.dump()
        return False
    
    # Find category name and return Category obj
    def findCategory(self, categoryName):
        return _findCat(self.topLevelCategories, categoryName)
    
    def flush(self):
        self.db.dump()
    
    def _getChoices(self):
        choices = []
        def addChoices(cat, spacing=''):
            choices.append(spacing + cat.name)
            for c in cat.children:
                addChoices(c, spacing + '  ')
        for cat in self.topLevelCategories:
            addChoices(cat)
        return choices
    
    def _presentCategoryChoice(self, t):
        msg = 'Select category for: ' + t.name
        choices = self._getChoices()
        reply = choicebox(msg, choices = choices)
        if reply: return reply.strip()
        else: return reply
    