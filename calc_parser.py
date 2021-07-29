import re
from specials import *

#holds the different types of tokens
op = "operator"
num = 'number'
br = 'bracket'
spec = 'special'

#stores the patterns that are searched for in the input text and there corresponding token type
patterns = [
        [r"[0-9]+[.]?[0-9]?", num],
        [r"[+-/*,]", op],
        [r"[()]", br],
        [r"([a-zA-Z]+):", spec]
    ]

# Converts input text into tokens these tokens look like: [type, value]
def lexer(t):
    pos = 0
    l = []
    while pos < len(t):
        match = None
        for pat in patterns:
            p = re.compile(pat[0])
            match = p.match(t, pos)
            if match:
                token = [match.group(0), pat[1]]
                l.append(token)
                pos = match.end(0)
                break
        if match == None:
            pos += 1
    return l

#Walks trough the tokens and tries to parse them with all parsers stored in the parsers variable
#This way extra parsers can be added with minor changes
#The lower index parser has priority
def parse(ops):
    for par in parsers:
        i = 0
        while i < len(ops):
            parser = par.make(ops[i:]) # make a new parser with the list after i
            if parser.isCorrect(): 
                ops[i] = parser
                aant = parser.consume()
                for a in range(i+1, i+aant): #remove the consumed items
                    del ops[i+1]
            else:
                i += 1

# basic operation class
class Operation():
    def __init__(self, ops):
        self.ops = ops
    def parse(self):
        parse(self.ops)
    #calculates the result of the containing operator
    def calculate(self):
        return self.ops[0].calculate()

# used to represent numbers
class Number(Operation):
    def __init__(self, ops):
        super().__init__(ops)
        self.ops = self.ops[:self.consume()].copy() # only keep the needed part of the list
    #used to create a new number from a list
    def make(self, ops):
        return Number(ops)
    # used in the parse routine to see if the tokens can be parsed with this parser
    def isCorrect(self):
        if len(self.ops)>=self.consume():
            if isinstance(self.ops[0], list):
                return  self.ops[0][1] == num
    # returns how much items this operation type uses
    def consume(self):
        return 1
    def calculate(self):
        return float(self.ops[0][0])
        
# parent class to represent operations that look like x + y where + can be any token of type "operant"
class Math(Operation):
    def __init__(self, ops):
        super().__init__(ops)
        self.ops = self.ops[:self.consume()].copy()
    def isCorrect(self):
        if len(self.ops)>=self.consume():
            if isinstance(self.ops[1], list):
                return  self.ops[1][1] == op
    def consume(self):
        return 3

# used to calculate x * y
class MathMul(Math):
    def make(self, ops):
        return MathMul(ops)
    def calculate(self):
        return super().calculate() * self.ops[2].calculate()
    def isCorrect(self):
        return super().isCorrect() and self.ops[1][0] == "*"

# used to calculate x + y
class MathAdd(Math):
    def make(self, ops):
        return MathAdd(ops)
    def calculate(self):
        return super().calculate() + self.ops[2].calculate()
    def isCorrect(self):
        return super().isCorrect() and self.ops[1][0] == "+"

# used to calculate x - y
class MathSub(Math):
    def make(self, ops):
        return MathSub(ops)
    def calculate(self):
        return super().calculate() - self.ops[2].calculate()
    def isCorrect(self):
        return super().isCorrect() and self.ops[1][0] == "-"

# used to calculate x / y
class MathDiv(Math):
    def make(self, ops):
        return MathDiv(ops)
    def calculate(self):
        return super().calculate() / self.ops[2].calculate()
    def isCorrect(self):
        return super().isCorrect() and self.ops[1][0] == "/"

# used to calculate x , y
# returns a list with the 2 values
# only used with brackets for special functions like: example:(1,2)
class Comma(Math):
    def make(self, ops):
        return Comma(ops)
    def calculate(self):
        return [super().calculate() , self.ops[2].calculate()]
    def isCorrect(self):
        return super().isCorrect() and self.ops[1][0] == ","

# used to represent everything in brackets
# takes everithing between the opening bracket and its closing bracket and parses the contents afterwards
class Bracket(Operation):
    def __init__(self, ops):
        super().__init__(ops)
        self.ops = self.ops[:self.findCloseBrack()+1].copy()
    def make(self, ops):
        return Bracket(ops)
    def isCorrect(self):
        if len(self.ops)>=2:
            if isinstance(self.ops[0], list):
                return  self.ops[0][0] == "(" and self.ops[-1][0] == ")"
    # finds the correct closing bracket used in init
    def findCloseBrack(self):
        depth = 1
        i = 0
        for i in range(1, len(self.ops)):
            if isinstance(self.ops[i], list):
                if self.ops[i][0] == '(':
                    depth += 1
                elif self.ops[i][0] == ')':
                    depth -= 1
            if depth == 0:
                break
        return i
    # deletes the open and closing bracket to prepare the list for further parsing
    # returns the length of the containing list with brackets
    def consume(self):
        l = len(self.ops)
        self.ops = self.ops[1:-1]
        self.parse()
        return l
    def calculate(self):
        return self.ops[0].calculate()

# used to represent special functions
# these can be called by typing a name followed by a : before the value you wish to pass
# for example:     function:1     or     pow:(1,2)
# you can also use a calculation as a argument to the function by putting it in brackets
# for example       function:(1+1)
class Special(Operation):
    def __init__(self, ops):
        super().__init__(ops)
        self.ops = self.ops[:self.consume()].copy()
    def make(self, ops):
        return Special(ops)
    def isCorrect(self):
        if len(self.ops)>=self.consume():
            if isinstance(self.ops[0], list):
                return  self.ops[0][1] == spec
    def consume(self):
        return 2
    # reads the specialDict dictionary from the imported specials.py 
    # in this file all special functions and there calling string are stored
    # this way adding new functions is simple and only requires changes to special.py
    def calculate(self):
        return specialDict[self.ops[0][0][:-1]](self.ops[1].calculate())

#stores all parsers and there order
parsers = [
    Bracket([]),
    Number([]),
    Special([]),
    Comma([]),
    MathMul([]),
    MathDiv([]),
    MathAdd([]),
    MathSub([]),
]

# the function that can be used externally to calculate the result of a given string
def calculate(text):
    operation = Operation(lexer(text))
    operation.parse()
    return operation.calculate()
