import numpy as n
from time import perf_counter

# Const Definitions
pi = 3.141592653589793
e =  2.718281828459045
twoPi = 6.283185307179586

# Function definitions
# Arithmetic
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x*y

def div(x, y):
    return x/y

def mod(x, y):
    return x % y

def power(base, exponent):
    return base**exponent

# Trig
def sin(x):
    sign: int = 1
    # Use properties of sin to reduce the value of x and also increase accuracy by bringing the value closer to 0
    while x > twoPi:
        x -= twoPi
    while x < -twoPi:
        x += twoPi
    
    if x > pi:
        x -= pi
        sign = -1
    elif x < -pi:
        x += pi
        sign = -1

    out = 0
    do = x                   # do stands for the change or delta in output by adding a new term
    # Taylor series expansion of sin: x - x^3/3! + x^5/5! - x^7/7! + ...
    # 50 terms are used which just about gives enough accuracy to be correct to the last few decimal places python can handle
    for i in range(3,100,2):
        out += do
        do *= -(x**2)/(i*(i-1))
    return sign*(out + do)

def cos(x):
    sign = 1
    # Use properties of cos to reduce the value of x and also increase accuracy by bringing the value closer to 0
    while x > twoPi:
        x -= twoPi
    while x < -twoPi:
        x += twoPi
    
    if x > pi:
        x -= pi
        sign = -1
    elif x < -pi:
        x += pi
        sign = -1

    out = 0
    do = 1                   # do stands for the change or delta in output by adding a new term
    # Taylor series expansion of sin: 1 - x^2/2! + x^4/4! - x^6/6! + ...
    # 50 terms are used which just about gives enough accuracy to be correct to the last few decimal places python can handle
    for i in range(2,100,2):
        out += do
        do *= -(x**2)/(i*(i-1))
    return sign*(out+do)

def tan(x):
    return sin(x)/cos(x)

def sec(x):
    return 1/cos(x)

def cot(x):
    return cos(x)/sin(x)

def cosec(x):
    return 1/sin(x)

# Other
def exp(x):
    return e**x

def abs(x):
    if x < 0:
        return -x
    return x

def factorial(x):
    if (x == 0):
        return 1

    out = 1
    for i in range(x,1,-1):
        out *= i
    return out

def log10(x):
    return n.log10(x)

def ln(x):
    return n.log10(x)/n.log10(e)

def sqrt(x):
    return x**(0.5)

# Hyperbolic trig

def sinh(x):
    return (exp(x)-exp(-x))/2

def cosh(x):
    return (exp(x)+exp(-x))/2

def tanh(x):
    return sinh(x)/cosh(x)

def sech(x):
    return 1/cosh(x)

def coth(x):
    return cosh(x)/sinh(x)

def cosech(x):
    return 1/sinh(x)

# Permutations and combinations

def nPr(n, r):
    return factorial(n)/(factorial(n-r))

def nCr(n, r):
    return factorial(n)/(factorial(r)*factorial(n-r))

# Inverse trig
def arcsin(x):
    return n.arcsin(x)

def arccos(x):
    return n.arccos(x)

def arctan(x):
    return n.arctan(x)

def arcsinh(x):
    return n.arcsinh(x)

def arccosh(x):
    return n.arccosh(x)

def arctanh(x):
    return n.arctanh(x)


n.sin
if __name__ == "__main__":

    for i in range(0,11,1):
        print(f"{i = }",end="\t")
        start_timeN = perf_counter()
        print(n.exp(i), end ="\t")
        end_timeN = perf_counter()
        start_timeC = perf_counter()
        print(exp(i))
        end_timeC = perf_counter()
        print(f"Code exuction time(Numpy): {(end_timeN - start_timeN)*1000:.4f}ms")
        print(f"Code exuction time(Custom): {(end_timeC - start_timeC)*1000:.4f}ms\n")