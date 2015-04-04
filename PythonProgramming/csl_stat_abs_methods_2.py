class Pizza:
    def __init__(self, size):
        self.size = size

    def get_size(self):
        return self.size

    @staticmethod
    def mix_ingredients(x, y):
        return x + y

    def cook(self):
        return self.mix_ingredients(self.cheese, self.vegetables)

    radius = 42

    @classmethod
    def get_radius(cls):
        return cls.radius


class MyDate:
    # day = month = year = 0

    total_dates_created =0

    @classmethod
    def giv_tot_dates(cls):
        return cls.total_dates_created

    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

        MyDate.total_dates_created += 1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        cls.total_dates_created += 1
        return cls(day, month, year)



class Parent:
    def method_1(self):
        raise NotImplementedError
    def method_2(self):
        raise NotImplementedError

class Child(Parent):
    def method_1(self):
        return "method_1 called"


from abc import ABCMeta, abstractmethod

class Base(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass

    @abstractmethod
    def bar(self):
        pass

class Concrete(Base):
    def foo(self):
        pass


def main():
    pass

if __name__ == "__main__":
    print("{}".format(Pizza.get_radius))

    print("{}".format(Pizza.get_radius()))

    my_date = MyDate.from_string("23-03-15")
    print("{}/{}/{}".format(my_date.day, my_date.month, my_date.year))

    date_string = "23-03-15"
    print("Is {} valid? {}.".format(date_string, MyDate.is_date_valid(date_string)))

    print("="*10)
    ch = Child()
    print(ch.method_1())

    # print(ch.method_2())

    print("="*10)

    print("TOT DATES: {}".format(MyDate.giv_tot_dates()))

    print("="*10)


    conc = Concrete()
