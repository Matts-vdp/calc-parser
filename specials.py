# This file contains all special functions
# when adding a new function you only have to make a new class and add it to the specialDict


# calculates the square root of the arg
# use sqrt:number to calculate the sqrt of the number
class Sqrt():
    def __call__(self, arg):
        return arg ** 0.5

# used to calculate powers of numbers from a list with 2 items
# to pass the items use pow:(item1, item2)
class Power():
    def __call__(self, arg):
        return arg[0] ** arg[1]

# stores all special functions and there invokation string
specialDict = {
    "sqrt": Sqrt(),
    "pow": Power(),
}