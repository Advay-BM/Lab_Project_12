import numpy as n
# from time import perf_counter

# Const Definitions
pi = 3.141592653589793
e =  2.718281828459045
twoPi = 6.283185307179586

# Whenever floating point comparisons are needed,
# we subtract the number from the number we want to compare to and check if that difference is less than epsilon
# if yes, the 2 numbers are close enough to be considered as equal
# This is needed due to floating point imprecision
epsilon = 0.0000000001

# Note: Overflow errors are used to indicate domain errors

# Function definitions
# Trig
def sin(x, rad = True):
    # Convert to radian if input is in degrees
    if not (rad):
        x = x*pi / 180

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
    do = x                  # do stands for the change or delta in output by adding a new term

    # Taylor series expansion of sin x: x - x^3/3! + x^5/5! - x^7/7! + ...
    # 50 terms are used which just about gives enough accuracy to be correct to the last few decimal places python can handle
    for i in range(3,100,2):
        out += do
        do *= -(x**2)/(i*(i-1))
    return sign*(out + do)

def cos(x, rad = True):
    # Convert to radian if input is in degrees
    if not (rad):
        x = x * pi / 180

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
    # Taylor series expansion of cos x: 1 - x^2/2! + x^4/4! - x^6/6! + ...
    # 50 terms are used which just about gives enough accuracy to be correct to the last few decimal places python can handle
    for i in range(2,100,2):
        out += do
        do *= -(x**2)/(i*(i-1))
    return sign*(out+do)

def tan(x, rad = True):
    if not (rad):
        x = x*pi / 180

    while x > pi:
        x -= pi
    while x < -pi:
        x += pi

    # Tan pi/2 and tan -pi/2 are +-infinity
    if (abs(pi/2 - x) <= epsilon):
        return float('inf')
    elif (abs(pi/2 + x) <= epsilon):
        return float('inf')

    return sin(x)/cos(x)

def sec(x, rad = True):
    if not (rad):
        x = x*pi / 180

    while x > twoPi:
        x -= twoPi
    while x < 0:
        x += twoPi

    if (abs(pi/2 - x) <= epsilon):
        return float('inf')
    elif (abs(3*pi/2 - x) <= epsilon):
        return float('inf')

    return 1/cos(x)

def cot(x, rad = True):
    if not (rad):
        x = x*pi / 180

    while x > pi:
        x -= pi
    while x < 0:
        x += pi

    if (abs(pi - x) <= epsilon):
        return float('inf')
    elif (abs(x) <= epsilon):
        return float('inf')

    return cos(x)/sin(x)

def csc(x, rad = True):
    if not (rad):
        x = x*pi / 180

    while x > twoPi:
        x -= twoPi
    while x < 0:
        x += twoPi

    if (abs(pi - x) <= epsilon):
        return float('inf')
    elif (abs(twoPi - x) <= epsilon):
        return float('inf')
    elif (abs(x) <= epsilon):
        return float('inf')

    return 1/sin(x)

# Hyperbolic trig
def sinh(x, rad = True):
    if not (rad):
        x = x*pi / 180

    # sinh = (e^x - e^(-x))/2 by definition
    return (exp(x)-exp(-x))/2

def cosh(x, rad = True):
    if not (rad):
        x = x*pi / 180

    # cosh = (e^x + e^(-x))/2 by definition
    return (exp(x)+exp(-x))/2

def tanh(x, rad = True):
    if not (rad):
        x = x*pi / 180

    return sinh(x)/cosh(x)

def sech(x, rad = True):
    if not (rad):
        x = x*pi / 180

    return 1/cosh(x)

def coth(x, rad = True):
    if not (rad):
        x = x*pi / 180

    return cosh(x)/sinh(x)

def csch(x, rad = True):
    if not (rad):
        x = x*pi / 180

    return 1/sinh(x)

# Inverse trig
def asin(x, rad = True):
    if x > 1 or x < -1:
        raise OverflowError

    result = n.arcsin(x)
    # Convert answer to degrees as the answer is in radians by default
    if not (rad):
        result = result*180 / pi

    return result

def acos(x, rad = True):
    if x > 1 or x < -1:
        raise OverflowError

    result = n.arccos(x)
    if not (rad):
        result = result*180 / pi

    return result
def atan(x, rad = True):
    result = n.arctan(x)
    if not (rad):
        result = result*180 / pi

    return result

def asec(x, rad = True):
    if x < 1 and x > -1:
        raise OverflowError

    result = n.arccos(1/x)
    if not (rad):
        result = result*180 / pi

    return result

def acot(x, rad = True):
    result = n.arctan(1/x)
    if not (rad):
        result = result*180 / pi

    return result

def acsc(x, rad = True):
    if x < 1 and x > -1:
        raise OverflowError

    result = n.arcsin(1/x)
    if not (rad):
        result = result*180 / pi

    return result

def asinh(x, rad = True):
    result = n.arcsinh(x)
    if not (rad):
        result = result*180 / pi

    return result

def acosh(x, rad = True):
    if x < 1:
        raise OverflowError

    result = n.arccosh(x)
    if not (rad):
        result = result*180 / pi

    return result

def atanh(x, rad = True):
    if x >= 1 or x <= -1:
        raise OverflowError

    result = n.arctanh(x)
    if not (rad):
        result = result*180 / pi

    return result

def asech(x, rad = True):
    if x <= 0 or x > 1:
        raise OverflowError

    result = n.arccosh(1/x)
    if not (rad):
        result = result*180 / pi

    return result

def acoth(x, rad = True):
    if x <= 1 and x >= -1:
        raise OverflowError

    result = n.arctanh(1/x)
    if not (rad):
        result = result*180 / pi

    return result

def acsch(x, rad = True):
    if x == 0:
        raise OverflowError

    result = n.arcsinh(1/x)
    if not (rad):
        result = result*180 / pi

    return result

# Other
def exp(x):
    return e**x

def mod(x):
    if x < 0:
        return -x
    return x

def factorial(x):
    # Raise error if x is not an integer but continue if its close enough
    if ((abs(x - n.floor(x)) > epsilon) and (abs(x - n.ceil(x)) > epsilon)):
        raise OverflowError

    # Do this so that it can be used as an argument for range
    x = int(x)

    # Negative factorials are undefined
    if (x < 0):
        raise OverflowError

    # 0! = 1
    if (x == 0):
        return 1

    # Very simple factorial calculator
    out = 1
    for i in range(x,1,-1):
        out *= i
    return out

def log(x):
    # log of 0 (in any base) is -inf
    if x == 0:
        return float('-inf')

    # Negative logarithms (in any base) are undefined
    if x < 0:
        raise OverflowError

    return n.log10(x)

def ln(x):
    if x == 0:
        return float('-inf')

    if x < 0:
        raise OverflowError

    # Base conversion as numpy does not have a ln function
    return n.log10(x)/n.log10(e)

def sqrt(x):
    return x**(0.5)

# Converts Cartesion coordinates to polar coordinates
def Pol(x, y, rad = True):
    r = (x**2 + y**2)**(0.5)
    theta = n.atan2(y,x)

    if not rad:
        theta = theta*180 / pi
    return (r, theta)

# Converts polar coordinates to Cartesion coordinates
def Rec(r, theta, rad = True):
    if not rad:
        theta = theta*pi / 180

    x = r*cos(theta)
    y = r*sin(theta)
    return (x, y)

def nRoot(n, x):
    return x**(1/n)

def npr(n, r):
    return int(factorial(n)/(factorial(n-r)))

def ncr(n, r):
    return int(factorial(n)/(factorial(r)*factorial(n-r)))

# Old code for testing efficiency of approximated functions:
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