__author__ = 'mark'

import math

def simple_gen():
    for i in range(10):
        yield i

for val in simple_gen():
    print(val)

my_gen = simple_gen()

print(next(my_gen))
print(next(my_gen))
print(next(my_gen))
print(next(my_gen))

def is_prime(num):
    if num > 1:
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for cur in range(3, int(math.sqrt(num)+1), 2):
            if num % cur == 0:
                return False
        return True
    return False


def get_primes(num):
    while True:
        if is_prime(num):
            yield num
        num +=1


my_gen = get_primes(100)

print(next(my_gen))
print(next(my_gen))
print(next(my_gen))
print(next(my_gen))
print(next(my_gen))

