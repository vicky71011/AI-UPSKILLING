# raw strings

print(r"C:\new_folder")  # Output: C:\new_folder

text = ('Put several strings within parentheses '
    'to have them joined together.') # Output: Put several strings within parentheses to have them joined together.

word = "Python"

print(word[4:42]) # Output: on
print(word[4:])   # Output: on
print(word[42:])  # Output: ""

rgb = [255, 128, 0]
rgba = rgb # same reference, changes made in one will affect the other

rgba = rgb[:] # new reference, changes made in one will not affect the other, shallow copy

rgb[:] = [] # Output: [], removes all the elements from the list, but keeps the reference to the original list

# for statements

for w in word:
    print(w) # Output: P y t h o n

users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}
for user, status in users.copy().items(): # Output: Hans, Éléonore, 景太郎
    if status == 'inactive':
        del users[user] 

# range() function

for i in range(5): # Output: 0, 1, 2, 3, 4
    print(i) 

print(list(range(5, 10, 1))) # Output: [5, 6, 7, 8, 9], range(start, end, increment)

# else clause in for loops

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')

# match statement

status = 404
match status:
        case 400:
            print("Bad request")
        case 404:
            print("Not found")
        case 418:
            print("I'm a teapot")
        case _:
            print("Something's wrong with the internet")

# case 401 | 403 | 404:
    # return "Not allowed"

# enum

from enum import Enum
class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

color = Color(input("Enter your choice of 'red', 'blue' or 'green': "))

match color:
    case Color.RED:
        print("I see red!")
    case Color.GREEN:
        print("Grass is green")
    case Color.BLUE:
        print("I'm feeling the blues :(")


# functions

## function with default arguments
def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        reply = input(prompt)
        if reply in {'y', 'ye', 'yes'}:
            return True
        if reply in {'n', 'no', 'nop', 'nope'}:
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)

## function with mutable default arguments
# [1] [1, 2] [1, 2, 3]
def f(a, L=[]):
    L.append(a)
    return L

print(f(1))
print(f(2))
print(f(3))