__author__ = 'mark'

"""
A vector is basically an arrow that has a magnitude (a length) and a direction (an angle with respect to typically the
x axis). It usually is represented as an x,y pair, where the origin of the vector is a 0,0 and the head of the vector
is at the listed pair.

Here are some of the operations you can perform on a vector.

    vector addition. If V1 is (x,y) and V2 is (a,b), the V+W is (x+a,y+b), a vector

    vector multiplication by a scalar. if V1 is (x,y), the V*n is (x*n,y*n), a vector

    vector subtraction V-W is the same as V+(W*-1), a vector

    vector multiplication with another vector. There are two possibilities, dot product or cross product. We’ll do dot
    product. If V=(x,y) and W=(a,b), then V*W = x*a + y*b, a scalar. Thus the dot product yields a scalar, not a vector

    vector magnitude. The magnitude based on the Pythagorean theorem for a V=(x,y) says that the magnitude is the square
    root of (x2 + y2) .

Your Tasks

Make a vector class. Provide the operators

__init__ # constructor, takes 3 args: self,x,y . No return
__str__ # for printing, takes 1 arg self. Returns a string
__add__ # vector + vector. Takes 2 args, self and vector. Returns a new vector
__sub__ # vector – vector. Takes 2 args, self and vector. Returns a new vector
__mul__ # two possibilities. vector*integer or vector*vector (dot product). Get it to do just one of the two at first,
then see if you can use introspection to do both

magnitude # magnitude of the vector. One arg, self. Returns a float
"""

import math


class Point:
    """Class to define a 'point' object which has x/y cartesian coordinates and its associated methods."""

    def __init__(self, x=0.0, y=0.0):
        """Initial values for x and y, defaults 0.0 in both cases."""
        try:
            x = float(x)
            y = float(y)
        except ValueError as e:
            print("{}\nChanging 'x' & 'y' to zero".format(e))
            x = 0.0
            y = 0.0

        self.x = x
        self.y = y

    def __str__(self):
        return "({:.2f}, {:.2f})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def distance(self, other):
        """Calculates distance based on Pythagoras' theorem."""
        return math.sqrt((abs(self.x - other.x) ** 2 + abs(self.y - other.y) ** 2))

    def __add__(self, other):
        """Adds two points together. Overloads + operator."""
        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Point(self.x - other, x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y)

    def magnitude(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2))


p1 = Point(3.1, 4.0)
p2 = Point(6.5, 7.75)
p3 = p1 + p2
dist = p1.distance(p2)

print("Magnitide of {} is {}".format(p1, p1.magnitude()))

print("p1={}".format(p1))
p1.x += 2
print("p1={}".format(p1))
p1 += p2

print("p1={}, p2={}, p3={}, dist={:2f}".format(p1, p2, p3, dist))

p4 = Point(1.0, 1.0)
print("Magnitide of {} is {}".format(p4, p4.magnitude()))

p5 = Point(2, 4)
p6 = Point("a", "b")
p7 = Point(a, b)