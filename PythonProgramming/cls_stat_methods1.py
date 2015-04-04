import random
import abc

class DummyParent(object):
    __metaclass__ = abc.ABCMeta

    # An abstract method defines a method that is not implemented but must be implemented in a derived class. It's a
    # sort of contract or direction to the developer of the derived class that the method must be implemented but
    # doesn't prescribe how this is to be done.
    @abc.abstractmethod
    def say_hello(self):
        # return "hello"
        raise NotImplementedError

class Dummy(DummyParent):
    count = 0

    def __init__(self, identity):
        # assert issubclass(self.__class__, DummyParent)
        self.identity = identity
        self.__othernumber = Dummy.get_rand()
        Dummy.count += 1

    @property
    def othernumber(self):
        return self.__othernumber

    @othernumber.setter
    def othernumber(self):
        return "You can't set othernumber"

    # def say_hello(self):
    #     pass

    def __str__(self):
        return "My id is {}".format(self.identity)

    # Class methods are bound to the class not the object. In the following methods, the first merely returns a count of
    # objects of the appropriate type. The second makes a new object so by definition it doesn't exist when the method
    # is called.
    @classmethod
    def get_num(cls):
        return "Class method returns {}".format(cls.count)

    @classmethod
    def obj_from_date(cls, ddmmyy):
        if Dummy.is_date_valid(ddmmyy):
            tmp_id = ddmmyy[4:]+"-"+ddmmyy[2:4]+"-"+ddmmyy[0:2]
            return cls(tmp_id)
        else:
            return None

    # Note that a static method does not need the current object(self) or the class (cls). The static method could be
    # defined outside the class as a function but it's more convenient to have it defined in the class as every object
    # finds it useful to inherit it. It can also be overridden if necessary
    @staticmethod
    def get_rand():
        return "Static method returns {}".format(random.randint(1, 20))

    @staticmethod
    def is_date_valid(ddmmyy):
        day, month, year = int(ddmmyy[:2]), int(ddmmyy[2:4]), int(ddmmyy[4:])
        return day <= 31 and month <= 12 and year <= 99


d1 = Dummy('a')
d2 = Dummy('b')

print("d1.count ", d1.count)
print("d2.count ", d2.count)
print("d1.identity ",d1.identity)
print("d2.identity ",d2.identity)
print("Dummy.get_rand() ",Dummy.get_rand())
print("d1.get_rand() ",d1.get_rand())
print("d1.get_num() ",d1.get_num())
print("Dummy.get_num() ", Dummy.get_num())
d3 = Dummy.obj_from_date("230499")
print(d3)
d4 = Dummy.obj_from_date("440499")
print(d4)
print("Dummy.obj_from_date('230499')", d3)
print("Dummy.is_date_valid('320499')", Dummy.is_date_valid("320499"))
print("Dummy.is_date_valid('230499')", Dummy.is_date_valid("230499"))
# d1.say_hello()