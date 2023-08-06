from sympy import *
from sympy.geometry import point

# class NewLine():
#     def __init__(self, point1: point, point2: point):
#         self.x, self.y = symbols('x y')

#         self.line = Line(point1, point2)
    
#     def get_perpendicular(self, intercept_point):
#         return NewLine(intercept_point, (self.line[1].y-self.line[0].y)/(self.line[1].x-self.line[0].x))
    
#     def getslope(self):
#         return self.line.slope()
    
#     def get_x_intercept(self):
#         return "Not Yet Implemented"
    
#     def __str__(self):
#         return str(self.line)
    
#     def getfunc(self, fname):
#         return eval("self."+fname)


def get_perp(line: Line2D, startpoint: point):
    if line.slope % 1 == 0:
        return Line(startpoint, slope=1/line.slope)
    else:
        return Line(startpoint, slope=line.slope.denominator/line.slope.numerator)