''' This example shows how to decorate any function, regardless of what parameters it requires. 'args'(note the
preceeding '*') is a variable that takes zero or more positional arguments, 'kwargs' (note the preceeding '**') is a
variable that takes zero or more key/value arguments.
'''

__author__ = 'mark'

def my_decorator(func_to_decorate):
    def my_wrapper(*args, **kwargs):
        print("In wrapper, wrapping {}".format(func_to_decorate.__name__))
        result = func_to_decorate(*args, **kwargs)
        print("Still in wrapper, returning wrapped {}".format(func_to_decorate.__name__))
        return result
    return my_wrapper

# decorate add_list1
@my_decorator
def add_list1 (int_list):
    result_sum=0
    for num in int_list:
        result_sum = result_sum + num
    print("In add_list1, res is {}".format(result_sum))
    return result_sum

# @timer_decorator, comment out decoration...
def add_list2(int_list):
    return sum(int_list)

# ...and do it by hand
add_list2 = my_decorator(add_list2)

@my_decorator
def print_stuff(str_var):
    print("In print_stuff...")
    return "print_stuff, val is {}".format(str_var)



int_list = list(range(5))

print(add_list1(int_list))
print(add_list2(int_list))
print(print_stuff("random junk"))