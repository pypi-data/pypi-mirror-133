# this is an example extension 

### when making an extension remember to add it to __init__.py

from sympy import sqrt # import sqaure root function from math library
from sympy import sympify # turn string into sympy expression

def triple(x):
    return 3*x

def inverse_sqrt(x):
    return sympify('1/sqrt('+str(x)+')').evalf()