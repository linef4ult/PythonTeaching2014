__author__ = 'mark'

def add(x,y):
    return x + y

def sub(x,y):
    return x - y

def apply(func, x, y):
    return func(x,y)

def outer():
    x = 1
    def inner():
        print("inner {}".format(x))
    return inner


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "Coord: " + str(self.__dict__)
    def __repr__(self):
        return self.__str__()

def add_c(a, b):
    return Coordinate(a.x + b.x, a.y + b.y)

def sub_c(a, b):
    return Coordinate(a.x - b.x, a.y - b.y)

def wrapper(func):
    def checker(a, b): # 1
        if a.x < 0 or a.y < 0:
            a = Coordinate(a.x if a.x > 0 else 0, a.y if a.y > 0 else 0)
        if b.x < 0 or b.y < 0:
            b = Coordinate(b.x if b.x > 0 else 0, b.y if b.y > 0 else 0)
        ret = func(a, b)
        if ret.x < 0 or ret.y < 0:
            ret = Coordinate(ret.x if ret.x > 0 else 0, ret.y if ret.y > 0 else 0)
        return ret
    return checker

def generic_logger(func):
    def inner(*args, **kwargs):
        print("Arguments passed to {} were: {}, {}".format(func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return inner


def wrapper_function(func):
    def inner(*args, **kwargs):
        print("Im just giving you back the stuff sent in to {}".format(func.__name__))
        print("The arguments were {} and {}".format(args, kwargs))

        # The next line runs the original function
        return func(*args, **kwargs)
    return inner


@generic_logger
def f1(x, y=1):
    return x * y

@generic_logger
def f2():
    return "stuff"

class P:

    def __init__(self,x):
        self.__x = x

    def __str__(self):
        return "x={}".format(self.x)

    def __repr__(self):
        self.__str__()

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x

def main():
    print("{}".format(apply(add,2,1)))
    print("{}".format(apply(sub,2,1)))

    foo = outer()
    foo()
    print("Closure: {}".format(foo.__closure__))


    one = Coordinate(100, 200)
    two = Coordinate(300, 200)
    three = add_c(one, two)
    print("one: {}".format(one))
    print("two: {}".format(two))
    print("three: {}".format(three))

    add_cc = wrapper(add_c)
    sub_cc = wrapper(sub_c)
    print("decorated one - two: {}".format(sub_cc(one, two)))
    print("decorated one + three: {}".format(add_cc(one, three)))

    f1(5,4)
    f1(1)
    f2()


    p1 = P(555)
    p2 = P(-10)
    p3 = P(1200)

    print("p1: {}, p2: {}, p3: {}".format(p1,p2,p3))

    print("="*10)

    print(f1(5,4))

if __name__ == "__main__":
    main()