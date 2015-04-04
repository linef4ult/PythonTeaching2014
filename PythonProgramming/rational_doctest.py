__author__ = 'mark'

# simple Rational number class

import sys


def gcd(a, b):
    """
    Function to compute greatest common divisor (gcd) of two integers.

    In mathematics, the greatest common divisor (gcd) of two or more integers, when at least one of them is not zero,
    is the largest positive integer that divides the numbers without a remainder. For example, the GCD of 8 and 12 is 4.

    :param a: Positive integer greater than zero
    :param b: Positive integer greater than zero
    :return: Integer result
    """

    print("In function gcd. Attempting to compute gcd for {} and {}".format(a, b))
    try:
        if not (isinstance(a, int) and a > 0):
            raise TypeError("Error in function gcd: a must be positive integer > 0")
        if not (isinstance(b, int) and a > 0):
            raise TypeError("Error in function gcd: b must be positive integer > 0")
    except TypeError as e:
        print(e)

    # Ensure that a > b, if it is not reverse a & b
    if not a > b:
        a, b = b, a

    print("Initial fraction is {}/{}".format(a, b))
    while b != 0:
        rem = a % b
        a, b = b, rem
        print(("{}/{}".format(a, b)))

    print("GCD is {}".format(a))
    return a


def lcm(a, b):
    """
    Function to compute least common multiple (lcm) of two numbers.

    In arithmetic and number theory, the least common multiple (also called the lowest common multiple or smallest
    common multiple) of two integers a and b,  is the smallest positive integer that is divisible by both a and b.
    Since division of integers by zero is undefined, this definition has meaning only if a and b are both different
    from zero. The LCM is also known as the "lowest common denominator" (LCD) that must be determined before fractions
    can be added, subtracted or compared.

    This function uses the gcm function.

    :param a: Positive integer greater than zero
    :param b: Positive integer greater than zero
    :return: Integer result
    """

    print("In function lcm. Attempting to compute lcm for {} and {}".format(a, b))
    try:
        if not (isinstance(a, int) and a > 0):
            raise TypeError("Error in function lcm: a must be positive integer > 0")
        if not (isinstance(b, int) and a > 0):
            raise TypeError("Error in function lcm: b must be positive integer > 0")
    except TypeError as e:
        print(e)

    print("LCM is {}".format(a * b // gcd(a, b)))
    return (a * b // gcd(a, b))


class Rational(object):
    """
    Implements a Rational number. This is defined as a fraction represented by two positive integers greater than zero.
    """

    def __init__(self, numer, denom=1):
        """

        :param numer: Positive integer greater than zero
        :param denom: Positive integer greater than zero, defaults to 1
        :return: nothing but exception status if appropriate
        """
        print("in __init__ method")

        try:
            if not (isinstance(numer, int) and numer>0):
                raise TypeError("numerator must be integer greater than 0")
            if not (isinstance(denom, int) and denom>0):
                raise TypeError("denominator must be integer greater than 0")
        except TypeError as e:
            print(e)

        self.numer = numer
        self.denom = denom

    def __str__(self):
        """ String representation for printing"""
        return str(self.numer) + '/' + str(self.denom)  # print as a fraction

    def __repr__(self):
        """ Representation of Rational number"""
        return self.__str__()

    def __add__(self, f):
        """ Add two Rationals"""
        print('in __add__ method')
        try:
            if type(f) == int:  # convert ints to Rationals
                f = Rational(f)
            if type(f) == Rational:
                # find a common denominator (lcm)
                theLcm = lcm(self.denom, f.denom)
                # multiply to make denominators the same, then add numerators
                theSum = (theLcm / self.denom * self.numer) + \
                         (theLcm / f.denom * f.numer)
                return Rational(int(theSum), theLcm)
            else:
                # print('wrong type')  # problem: some type we cannot handle
                raise TypeError("{} id of incorrect type".format(f))
        except TypeError as e:
            print(e)

    def __radd__(self, f):
        """ Add two Rationals (reversed)"""
        # mapping is reversed: if "1 + x", x maps to self, and 1 maps to f
        print("in __radd__ method")
        # mapping is already reversed so self will be Rational; call __add__
        return self.__add__(f)

    def __iadd__(self, i):
        '''Increment'''
        print("in __iadd__ method")
        return self.__add__(i)

    def __sub__(self, f):
        """ Subtract two Rationals"""
        print('in __sub__ method')
        # subtraction is the same as addition with "+" changed to "-"
        theLcm = lcm(self.denom, f.denom)
        numeratorDiff = (theLcm / self.denom * self.numer) - \
                        (theLcm / f.denom * f.numer)
        return Rational(int(numeratorDiff), theLcm)

    def reduce(self):
        """ Return the reduced fractional value."""
        print('in reduce method')
        # find the gcd and then divide numerator and denominator by gcd
        thegcd = gcd(self.numer, self.denom)
        return Rational(self.numer // thegcd, self.denom // thegcd)

    def __eq__(self, f):
        """ Compare two Rationals for equality"""
        print('in __eq__ method')
        # reduce both; then check that numerators and denominators are equal
        f1 = self.reduce()
        f2 = f.reduce()
        return f1.numer == f2.numer and f1.denom == f2.denom



def main():
    aa = Rational(1, 2)
    bb = Rational(5, 10)

    aa == bb

    cc = Rational(2, 3)

    aa + bb
    aa + 2
    aa += cc

    gcd(0, 1)

if __name__ == "__main__":
    main()
