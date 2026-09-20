# from time import perf_counter

# Const Definitions (18 decimal places which is the upper limit of precision for python)
pi = 3.141592653589793238
e =  2.718281828459045235
twoPi = 6.283185307179586476

# Whenever floating point comparisons are needed,
# we subtract the number from the number we want to compare to and check if that difference is less than epsilon
# if yes, the 2 numbers are close enough to be considered as equal
# This is needed due to floating point imprecision
epsilon = 0.00000000000001

# Note: Overflow errors are used to indicate domain errors

# Function definitions

def binSearch(fInv, x, left, right):
    """
    Approximates the value of the function f at x if its inverse and 2 x-coords to left and right of x are given by doing a binary search.
    For this to work effectively, f must be continuous and monotonically increasing/decreasing
    """
    mid = (left+right)/2
    approx = fInv(mid)

    while (abs(x-approx) > epsilon):
        if approx > x:
            right = mid
        elif approx < x:
            left = mid
        else:
            return mid
        mid = (left+right)/2
        # Break out if we're not able to go further
        if (a := fInv(mid)) == approx:
            break
        approx = a

    return mid

# Trig
# Error < 1E-14
def sin(x, rad = True):
    # Convert to radian if input is in degrees
    if not (rad):
        x = x*pi / 180

    sign: int = 1
    # Use properties of sin to reduce the value of x and also increase accuracy by bringing the value closer to 0
    while x > twoPi:
        x -= twoPi
    while x < 0:
        x += twoPi

    if x > pi:
        x -= pi
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

    return sin(x + pi/2)

# error < 1E-14 generally, can drop as low as 1E-6 for numbers close to odd multiples of pi/2
def tan(x, rad = True):
    if not (rad):
        x = x*pi / 180

    while x > pi/2:
        x -= pi
    while x < -pi/2:
        x += pi

    # Tan pi/2 and tan -pi/2 are +-infinity
    if (abs(pi/2 - x) <= epsilon):
        return float('inf')
    elif (abs(pi/2 + x) <= epsilon):
        return float('inf')

    if x == 0:
        return 0

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

    return tan(pi/2 - x)

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

    if (abs(x) <= epsilon):
        return float('inf')

    return cosh(x)/sinh(x)

def csch(x, rad = True):
    if not (rad):
        x = x*pi / 180

    if (abs(x) <= epsilon):
        return float('inf')

    return 1/sinh(x)

# Inverse trig
def asin(x, rad = True):
    if x > 1 or x < -1:
        raise OverflowError

    sign = 1
    if x < 0:
        x = -x
        sign = -1
    elif x == 0:
        return 0

    if (x == 1):
        return sign*pi/2

    if 1-x < 0.00001:
        return sign*(pi/2 + (x-1)*447.21397)

    y = binSearch(sin, x, 0, pi/2)
    y = y - (sin(y) - x)/cos(y)
    result = sign*y
    # Convert answer to degrees as the answer is in radians by default
    if not (rad):
        result = result*180 / pi

    return result

def acos(x, rad = True):
    # The domain check already happens in asin

    result = pi/2 - asin(x)

    if not (rad):
        result = result*180 / pi

    return result

def atan(x, rad = True):
    sign = 1
    if x < 0:
        x = -x
        sign = -1
    elif x == 0:
        return 0

    y = acos(1/((1+x*x)**0.5))
    y = y - cos(y)*(sin(y) - x*cos(y))
    if x > 200:
        for _ in range(10):
            y = y - cos(y)*(sin(y) - x*cos(y))
    result = sign*y

    if not (rad):
        result = result*180 / pi

    return result

def asec(x, rad = True):
    if x < 1 and x > -1:
        raise OverflowError

    result = acos(1/x)
    if not (rad):
        result = result*180 / pi

    return result

def acot(x, rad = True):
    result = pi/2 - atan(x)

    if not (rad):
        result = result*180 / pi

    return result

def acsc(x, rad = True):
    # The domain check already happens in asec

    result = pi/2 - asec(x)

    if not (rad):
        result = result*180 / pi

    return result

def asinh(x, rad = True):
    result = ln(x+(x*x+1)**(0.5))
    if not (rad):
        result = result*180 / pi

    return result

def acosh(x, rad = True):
    if x < 1:
        raise OverflowError

    result = ln(x+(x*x-1)**(0.5))
    if not (rad):
        result = result*180 / pi

    return result

def atanh(x, rad = True):
    if x >= 1 or x <= -1:
        raise OverflowError

    result = 0.5*ln((1+x)/(1-x))
    if not (rad):
        result = result*180 / pi

    return result

def asech(x, rad = True):
    if x <= 0 or x > 1:
        raise OverflowError

    result = acosh(1/x)
    if not (rad):
        result = result*180 / pi

    return result

def acoth(x, rad = True):
    if x <= 1 and x >= -1:
        raise OverflowError

    result = atanh(1/x)
    if not (rad):
        result = result*180 / pi

    return result

def acsch(x, rad = True):
    if x == 0:
        raise OverflowError

    result = asinh(1/x)
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

def sqrt(x):
    if x < 0:
        raise OverflowError

    return x**(0.5)

def factorial(x):
    # If I knew how to compute the gamma function, I absolutely would have done

    # Raise error if x is not an integer but continue if its close enough
    if ((abs(x - (x//1)) > epsilon) and (abs(x - (x//1 + 1)) > epsilon)):
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

# I could've made a general logarithmic function for any base but the change of base formula exists so I'm not going to

def log(x):
    # log of 0 (in any base) is -inf
    if x == 0:
        return float('-inf')

    # Negative logarithms (in any base) are undefined
    if x < 0:
        raise OverflowError

    left: float = 0
    right: float = 0
    if x > 1:
        right = 1
        while (10**right < x):
            right += 1
        left = right - 1
    elif x < 1:
        left = -1
        while (10**left > x):
            left -= 1
        right = left + 1
    else:
        return 0

    if 10**right == x:
        return right
    elif 10**left == x:
        return left

    return binSearch(lambda y: 10**y, x, left, right)

def ln(x):
    if x == 0:
        return float('-inf')

    if x < 0:
        raise OverflowError

    left: float = 0
    right: float = 0
    if x > 1:
        right = 1
        while (e**right < x):
            right += 1
        left = right - 1
    elif x < 1:
        left = -1
        while (e**left > x):
            left -= 1
        right = left + 1
    else:
        return 0

    if e**right == x:
        return right
    elif e**left == x:
        return left

    return binSearch(lambda y: e**y, x, left, right)

def atan2(y, x):
    if x > 0:
        return atan(y/x)
    elif x < 0 and y >= 0:
        return pi + atan(y/x)
    elif x < 0 and y < 0:
        return atan(y/x) - pi
    elif x == 0 and y > 0:
        return pi/2
    elif x == 0 and y < 0:
        return -pi/2
    else:
        return 0

# Converts Cartesion coordinates to polar coordinates
def Pol(x, y, rad = True):
    r = (x**2 + y**2)**(0.5)
    theta = atan2(y,x)

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
    if n <= 0 or type(n) != int:
        raise OverflowError

    if x < 0 and n % 2 == 0:
        raise OverflowError

    return x**(1/n)

def npr(n, r):
    return int(factorial(n)/(factorial(n-r)))

def ncr(n, r):
    return int(factorial(n)/(factorial(r)*factorial(n-r)))

# Old code for testing efficiency of approximated functions:
# if __name__ == "__main__":
#     yVals = []
#     xVals = []
#     print(ln(100_000))
#     for i in range(1,10_000,1):
#         xVals.append(i/10_000)
#         yVals.append(a := (abs(ln(i/10_000) - n.log(i/10_000))))
#         # if a > 1E-6:
#         #     print(i/1000,abs(cot(i/1000)))
#     plt.plot(xVals, yVals)
#     plt.yscale('log')
#     plt.xlim(1/10_000,1)
#     plt.ylim(0,10000)
#     plt.show()
    # print(f"{i = }",end="\t")
    # # start_timeN = perf_counter()
    # print(n.exp(i), end ="\t")
    # # end_timeN = perf_counter()
    # # start_timeC = perf_counter()
    # print(exp(i))
    # end_timeC = perf_counter()
    # print(f"Code exuction time(Numpy): {(end_timeN - start_timeN)*1000:.4f}ms")
    # print(f"Code exuction time(Custom): {(end_timeC - start_timeC)*1000:.4f}ms\n")