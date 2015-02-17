__author__ = 'mark'
# simple clock class


class Clock(object):
    """Simple clock class
    Takes hours, minutes, seconds as ints
    Can be updated by time in the form of 'hh:mm:ss'"""

    def __init__(self, hours=0, minutes=0, seconds=0):
        try:
            assert type(hours) == int and -1 < hours < 24
            assert type(minutes) == int and -1 < minutes < 60
            assert type(seconds) == int and -1 < seconds < 60
            self.hours = hours
            self.minutes = minutes
            self.seconds = seconds

        except AssertionError as e:
            self.hours = self.minutes = self.seconds = None
            print('AssertionError -- {}:{}:{}. Object values set to {}'.format(hours, minutes, seconds ,self))

    def __str__(self):
        return '{} hours, {} minutes and {} seconds'.format(self.hours, self.minutes, self.seconds)

    def __repr__(self):
        return self.__str__()

    def stringUpdate(self, str):
        hours, minutes, seconds = [int(n) for n in str.split(':')]
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __add__(self, other):
        carryMinutes, seconds = divmod((self.seconds + other.seconds), 60)
        carryHours, minutes = divmod((self.minutes + other.minutes), 60)
        carryDays, hours = divmod((self.hours + other.hours), 24)
        print('{} secs, {} carry mins, {} mins, {} carry hrs, {} hrs'.format(seconds, carryMinutes, minutes, carryHours,
                                                                             hours))
        return Clock(hours + carryHours, minutes + carryMinutes, seconds)


c0 = Clock(25, 77, 99)
c1 = Clock(23, 59, 10)
c2 = Clock(9, 20, 00)
c3 = c1 + c2
print('c1: {}'.format(c1))
print('c2: {}'.format(c2))
print('c3: {}'.format(c3))
c2.stringUpdate('11:23:45')
print('c2: {}'.format(c2))
