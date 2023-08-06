from sympy import pi, sqrt, Symbol, symbols, sympify, Eq
from sympy.solvers import solve

# class TanVelocity():
#     def __init__(self, radius=None, time=None, velocity=None):
#         self.r, self.t, self.v = symbols('r, t, v')

#         self.tanvelocity = {
#             "find_velocity": sympify("(2*pi*self.r)/self.t")
#         }

#         if radius != None:
#             return solve(self.tanvelocity["find_velocity"])
#         if time != None:
#             print("not yet implemented")
#         if velocity != None:
#             print('not yet implemented')
        
#     def __str__(self):
#         return solve(self.equ)

# expressions = {}

# very bad, will be removed
def tangential_velocity(radius=None, time=None, velocity=None):
    r, t, v = symbols('r t v')
    # tanq = Eq(((v)-(2*pi*r/t)), 0)
    # print(tanq)
    # print(solve(tanq))
    # print(tanq.subs(r, 12293).subs(t, 9.9259*60**2))
    # print(solve(tanq.subs(r, 12293).subs(t, 9.9259*60**2)))


    if velocity == None:
        return str(sympify("(2*pi*"+str(radius)+")/"+str(time)).evalf())
    if time == None:
        return str(sympify("2*pi/"+str(time)+"*"+str(velocity)).evalf())
    if radius == None:
        return str(sympify("2*pi/"+str(velocity)+"*"+str(time)).evalf())


def centripital_acceleration():
    pass
    


### old physics functions using gmpy2

# # tangential velocity
# # and its algebraic alternatives

# # return velocity (single dimension)
# def tan_velocity(radius: mpnum, time: mpnum):
#     return (mpnum(str(2*pi))*radius)/time

# # return velocity from acceleration and radius
# def velocity_from_tan(acceleration, radius):
#     return sqrt(acceleration*radius)

# # return radius from tangential acceleration
# def radius_from_tan(acceleration, velocity):
#     return velocity**2/acceleration


# # centripital acceleration and its
# # algebraic representations

# # returns acceleration
# def centripital_from_velocity(velocity: mpnum, radius: mpnum):
#     output = velocity.pow(2)/radius
#     return output

# # takes time for a revolution, and returns acceleration
# def centripital_from_time(time, radius):
#     output = (4*(pi**2)*radius)/(time**2)
#     return output

# # returns radius from centripital acceleration, and time
# def radius_from_centripital(acceleration, time):
#     return sqrt((time**2*acceleration)/(4*pi**2))

# # returns time from centripital acceleration, and radius
# def time_from_centripital(acceleration, radius):
#     return sqrt((4*pi**2*radius)/acceleration)