import numpy as n
import sympy as s
# from time import perf_counter

# Const Definitions
pi = 3.141592653589793
e =  2.718281828459045
twoPi = 6.283185307179586
epsilon = 0.0000000001
# Function definitions
# Arithmetic
def power(base, exponent): # type: ignore # type: ignore
    return base**exponent # type: ignore

# Trig
def sin(x): # type: ignore
    sign: int = 1
    # Use properties of sin to reduce the value of x and also increase accuracy by bringing the value closer to 0
    while x > twoPi:
        x -= twoPi # type: ignore # type: ignore
    while x < -twoPi:
        x += twoPi # type: ignore
    
    if x > pi:
        x -= pi # type: ignore # type: ignore
        sign = -1
    elif x < -pi:
        x += pi # type: ignore
        sign = -1

    out = 0
    do = x                   # type: ignore # type: ignore # do stands for the change or delta in output by adding a new term
    # Taylor series expansion of sin: x - x^3/3! + x^5/5! - x^7/7! + ...
    # 50 terms are used which just about gives enough accuracy to be correct to the last few decimal places python can handle
    for i in range(3,100,2):
        out += do # type: ignore # type: ignore
        do *= -(x**2)/(i*(i-1)) # type: ignore
    return sign*(out + do) # type: ignore

def cos(x): # type: ignore # type: ignore
    sign = 1
    # Use properties of cos to reduce the value of x and also increase accuracy by bringing the value closer to 0
    while x > twoPi:
        x -= twoPi # type: ignore
    while x < -twoPi:
        x += twoPi # type: ignore
    
    if x > pi:
        x -= pi # type: ignore
        sign = -1
    elif x < -pi:
        x += pi # type: ignore
        sign = -1

    out = 0
    do = 1                   # do stands for the change or delta in output by adding a new term
    # Taylor series expansion of sin: 1 - x^2/2! + x^4/4! - x^6/6! + ...
    # 50 terms are used which just about gives enough accuracy to be correct to the last few decimal places python can handle
    for i in range(2,100,2):
        out += do # type: ignore
        do *= -(x**2)/(i*(i-1)) # type: ignore
    return sign*(out+do) # type: ignore

def tan(x): # type: ignore
    while x > pi:
        x -= pi
    while x < -pi:
        x += pi
    if (abs(pi/2 - x) <= epsilon):
        return float('inf')
    elif (abs(pi/2 + x) <= epsilon):
        return float('inf')
    return sin(x)/cos(x) # type: ignore

def sec(x): # type: ignore # type: ignore
    while x > twoPi:
        x -= twoPi # type: ignore
    while x < 0:
        x += twoPi # type: ignore
    if (abs(pi/2 - x) <= epsilon):
        return float('inf')
    elif (abs(3*pi/2 - x) <= epsilon):
        return float('inf')
    return 1/cos(x) # type: ignore

def cot(x): # type: ignore
    while x > pi:
        x -= pi
    while x < 0:
        x += pi
    if (abs(pi - x) <= epsilon):
        return float('inf')
    elif (abs(x) <= epsilon):
        return float('inf')
    return cos(x)/sin(x) # type: ignore

def csc(x): # type: ignore
    while x > twoPi:
        x -= twoPi # type: ignore
    while x < 0:
        x += twoPi # type: ignore
    if (abs(pi - x) <= epsilon):
        return float('inf')
    elif (abs(twoPi - x) <= epsilon):
        return float('inf')
    elif (abs(x) <= epsilon):
        return float('inf')
    return 1/sin(x) # type: ignore

# Other
def exp(x): # type: ignore
    return e**x # type: ignore

def abs(x): # type: ignore
    if x < 0:
        return -x # type: ignore
    return x # type: ignore

def factorial(x): # type: ignore
    if (x == 0):
        return 1

    out = 1
    for i in range(x,1,-1): # type: ignore
        out *= i
    return out

def log(x): # type: ignore
    return n.log10(x) # type: ignore

def ln(x): # type: ignore
    return n.log10(x)/n.log10(e) # type: ignore

def sqrt(x): # type: ignore
    return x**(0.5) # type: ignore

def Pol(x, y): # type: ignore
    r = (x**2 + y**2)**(0.5) # type: ignore
    theta = n.atan2(y,x) # type: ignore
    return (r, theta) # type: ignore

def Rec(r, theta): # type: ignore # type: ignore
    x = r*cos(theta) # type: ignore
    y = r*sin(theta) # type: ignore
    return (x, y) # type: ignore

def nRoot(n, x): # type: ignore
    return x**(1/n) # type: ignore

# Hyperbolic trig

def sinh(x): # type: ignore
    return (exp(x)-exp(-x))/2 # type: ignore

def cosh(x): # type: ignore
    return (exp(x)+exp(-x))/2 # type: ignore

def tanh(x): # type: ignore
    return sinh(x)/cosh(x) # type: ignore

def sech(x): # type: ignore # type: ignore
    return 1/cosh(x) # type: ignore

def coth(x): # type: ignore
    return cosh(x)/sinh(x) # type: ignore

def csch(x): # type: ignore
    return 1/sinh(x) # type: ignore

# Permutations and combinations

def npr(n, r): # type: ignore
    return int(factorial(n)/(factorial(n-r))) # type: ignore

def ncr(n, r): # type: ignore
    return int(factorial(n)/(factorial(r)*factorial(n-r))) # type: ignore

# Inverse trig
def asin(x): # type: ignore
    if x > 1 and x < -1:
        raise OverflowError

    return n.arcsin(x) # type: ignore

def acos(x): # type: ignore
    if x > 1 and x < -1:
        raise OverflowError
    
    return n.arccos(x) # type: ignore

def atan(x): # type: ignore
    return n.arctan(x) # type: ignore

def asec(x): # type: ignore
    if x < 1 and x > -1:
        raise OverflowError
    
    return s.asec(x) # type: ignore

def acot(x): # type: ignore
    return s.cot(x) # type: ignore

def acsc(x): # type: ignore
    if x < 1 and x > -1:
        raise OverflowError

    return s.acsc(x) # type: ignore

def asinh(x): # type: ignore
    return n.arcsinh(x) # type: ignore

def acosh(x): # type: ignore
    if x < 1:
        raise OverflowError
    
    return n.arccosh(x) # type: ignore

def atanh(x): # type: ignore
    if x >= 1 and x <= -1:
        raise OverflowError
    
    return n.arctanh(x) # type: ignore

def assech(x): # type: ignore
    if x <= 0 and x > 1:
        raise OverflowError

    return s.asech(x) # type: ignore

def acoth(x): # type: ignore
    if x <= 1 and x >= -1:
        raise OverflowError

    return s.coth(x) # type: ignore

def acsch(x): # type: ignore
    if x == 0:
        raise OverflowError
    
    return s.acsch(x) # type: ignore

# if __name__ == "__main__":

#     for i in range(0,11,1):
#         print(f"{i = }",end="\t")
#         start_timeN = perf_counter()
#         print(n.exp(i), end ="\t")
#         end_timeN = perf_counter()
#         start_timeC = perf_counter()
#         print(exp(i))
#         end_timeC = perf_counter()
#         print(f"Code exuction time(Numpy): {(end_timeN - start_timeN)*1000:.4f}ms")
#         print(f"Code exuction time(Custom): {(end_timeC - start_timeC)*1000:.4f}ms\n")