# __________Data Types & Structures__________
integer = 1
float = 1.0
string = "Hello World"
boolean = True
none_var = None

# Structures:
list_var = [1, 2, 3, 4, 5] # List
tuple_var = (1, 2, 3, 4, 5) # Tuple
set_var = {1, 2, 3, 4, 5} # Set (unordered and unique values only, faster)
dict_var = {'key1': 'value1', 'key2': 'value2'} # Dictionary

# Python also supports type hints:
integer: int = 1
# If a variable of a given type can also be null, the following syntax is used:
from typing import Optional
integer: Optional[int] = None

name = "John"
age = 23
print(f"My name is {name} and I am {age} years old.") # String interpolation
print("My name is {} and I am {} years old.".format(name, age)) # String formatting




# __________Conditions__________
if age >= 18:
    print("I am an adult.")
elif age >= 13:
    print("I am a teenager.")
else:
    print("I am a child.")


match (age % 2):
    case 0:
        print("My age is even.") 
    case 1: 
        print("My age is odd.")
    case _:
        print("age is not an integer")


# Ternary operator (variable = value_if_true if expression else value_if_false):
status = "Adult" if age >= 18 else "Minor"




# __________Loops__________
for i in range(5):
    print(i)


i = 0
while i < 5:
    print(i)
    i += 1


names = ["John", "Rob", "Dan"]
for name in names:
    print(name)


names = [f"Mr. {name} Smith" for name in names] # List comprehension
for index, name in enumerate(names):
    print(f"{index}: {name}")




# __________Functions__________
def add(x, y): return x + y


# Lambda (anonymous) equivalent:
add = lambda x, y: x + y


# Default parameter value syntax:
def add(x, y, z=0): return x + y + z

# Generator function:
def fibonacci():
    # It's possible to declare multiple variables on one line:
    a, b = 0, 1
    while True:
        # The yield keyword returns a value and pauses the function, resuming from the same point when called again.
        # It also resumes from the same point when the next() function is called.
        yield a
        a, b = b, a + b


# The generator function returns an iterator. 
# The iterator can be used in a for loop, or with the next() function (which returns the next value in the iterator).
fibonacci_iterator = fibonacci()
index = 0
while index < 10:
    # Outputs 0, 1, 1, 2, 3, 5, 8, 13, 21, 34:
    print(next(fibonacci_iterator))
    index += 1


for number in fibonacci_iterator:
    # Outputs 55, 89, 144, 233, 377, 610, 987, 1597:
    print(number)
    if number >= 1000:break




# __________Decorators__________
# A decorator is a higher order function that takes another function as an argument, and extends its functionality without modifying it.
def simple_decorator(func):
    def wrapper():
        print("Before the function call")
        func()
        print("After the function call")

    # Returning a new function that wraps the argument function:
    return wrapper


# Applying the decorator:
@simple_decorator
def say_hello():
    print("Hello World")

# Including the decorator means that calling say_hello actually calls the simple_decorator function, passing the say_hello function as an argument.
# So the simple_decorator ends up returning the wrapper function.
# Then, Python replaces or 'decorates' the say_hello function with the wrapper function.
# So whenever say_hello is called, it actually calls the wrapper function.
# This is equivalent to: say_hello = simple_decorator(say_hello)
say_hello()


# Decorators can also take arguments. This is a decorator factory - returning a decorator function.
# Having a decorator with an argument requires another level of nesting.
# This is because the function following the '@' symbol must be a function that takes a function and returns a function.
# To make a decorator that takes an argument, we need to make a function that takes an argument,
# and returns a decorator function according to the argument value.
# In this example, the decorator takes an argument that specifies how many times the function should be called.
def repeat(calls):

    # This is the actual decorator being returned, which takes a function as an argument:
    def decorator_repeat(func):

        # This is the wrapper function that will replace the decorated function:
        def wrapper(*args, **kwargs):
            # Running the decorated function the specified number of times:
            for _ in range(calls):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

# Using the decorator factory to create a decorator that repeats the function the specified number times:
@repeat(calls=3)
def greet(name):
    print(f"Hello {name}")
greet("World")  # Outputs "Hello World" three times




# __________Error Handling__________
try:
    # Some code that throws an error:
    raise Exception("Some Error")
except Exception as exception:
    # Handling the error:
    print(exception)
finally: # Optional
    # This code executes regardless of whether an error is thrown.
    # It's useful for performing cleanup actions that must always be completed, 
    # such as manually closing a file not handled with 'with'.
    print("This code runs no matter what")


def divide(a, b):
    # Raising custom errors:
    if b==0: raise Exception("Cannot divide by zero")
    return a / b


# It is also possible to create custom error classes:
class CustomError(Exception): pass

try:
    raise CustomError("This is a custom error.")
except CustomError as error:
    print(error)




# __________Object-Oriented Programming__________
# A base class with 1 method
class Shape:
    def __init__(self, color):
        self.color = color

    def area(self):
        raise NotImplementedError


# A child class of Shape: 
class Rectangle(Shape):
    # Polymorphism through overriding:
    def __init__(self, color, height, width):
        # Calling the parent constructor:
        super().__init__(color)
        self.height = height
        self.width = width

    def area(self):
        return self.height * self.width


# A child class of Rectangle:
class Square(Rectangle):
    def __init__(self, color, side):
        # Calling the parent constructor:
        super().__init__(color, side, side)
    
    # Getter method:
    def get_side(self):
        return self.height
    
    # Setter method:
    def set_side(self, side):
        if side < 0: raise ValueError("Side cannot be negative")
        self.height = side
        self.width = side


my_square = Square("Blue", 10)
print(my_square.area()) # Outputs 100




# __________RegEx__________ 
# Regular expressions are used to find patterns within strings.
# It is commonly used to validate user input, and to find and replace text.
# The search pattern is defined between two slashes, and search flags can be added at the end.

# Flags:
# Whilst JS uses flags such as g, i, m, u, s, y, Python uses re.search(pattern, string, flags=0). TODO: CHANGE

# Special characters can be combined within the search expression to match more complex patterns:
#     "|": logical OR (to match one string or the other)
#     "()": group logic using parentheses
#     "[]": match any character within the brackets
#     "[^]": match any character not within the brackets (negation)

#     "\": escape especial character (to match special characters like the dot character)
#     "\d": match any digit
#     "\D": match any non-digit
#     "\w": match any alphanumeric character
#     "\W": match any non-alphanumeric character
#     "\s": match any whitespace character
#     "\S": match any non-whitespace character


# Quantifiers can be used to control how many times a character or group preceding the quantifier is matched:
#     "?": match 0 or 1 times
#     "*": match 0 or more times
#     "+": match 1 or more times
#     "{n}": match exactly n times
#     "{min, max}": match between the specified range (inclusive)

# There are more special characters and quantifiers, but these are the most common ones.

import re

search_string = "Hello World"

# r indicates a raw string (i.e. "\" is treated as an actual character rather than using /n, /t):
# Flags are set as the second argument of the compile method. Multiple can be used, separated by the logical OR.
regex = re.compile(r"hello", re.IGNORECASE | re.MULTILINE | re.DOTALL) 

# The 'search' method can be used for the first match, or 'findall' for all matches:
print(regex.findall(search_string))

# Use the 'sub' method to replace matches with a string:
print(regex.sub("Hi", search_string))
