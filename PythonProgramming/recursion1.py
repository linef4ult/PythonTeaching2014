__author__ = 'mark'

import turtle as t


def branch(length, level):
    if level <= 0:
        return
    t.forward(length)
    print("forward {:.2f}".format(length))
    t.left(45)
    print("1. left 45")
    branch(0.6 * length, level - 1)
    t.right(90)
    print("right 90")
    branch(0.6 * length, level - 1)
    t.left(45)
    print("2. left 45")
    t.backward(length)
    print("backward {:.2f}".format(length))
    return

def serpinski(length, depth):
    if depth > 1:
        t.dot()
    if depth == 0:
        t.stamp()
    else:
        serpinski_draw(length, depth)
        serpinski_draw(length, depth)
        serpinski_draw(length, depth)

def serpinski_draw(length, depth):
        t.forward(length)
        print("forward {}".format(length))
        serpinski(length/2, depth-1)
        t.backward(length)
        print("backward {}".format(length))
        t.left(120)
        print("left 120")


def factorial(n):
    print("Entered factorial n = " + str(n))
    if n == 1:
        return 1
    print("Before recursive call f(" + str(n) + ")")
    rest = factorial(n - 1)
    print("After recursive call f(" + str(n) + ")", rest)
    return n * rest


branch(100, 5)
# serpinski(200,6)
# factorial(4)
