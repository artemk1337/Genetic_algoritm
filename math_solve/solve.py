"""
a + 2b + 3c + 4d + 5e = 50
Can u find solve?

Maybe this?
a * b * 100 * exp(c) - 310 * d + 5 ** e = 1

"""

import sys
import math
import numpy as np
from random import randint


class GG(object):
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def solve_1(self):
        return abs((self.a + 2*self.b + 3*self.c + 4*self.d + 5*self.e) - 50)

    def solve_2(self):
        return abs(self.a * self.b * 100 * math.exp(self.c) - 310 * self.d + 5 ** self.e - 1)

    def get_koef(self):
        return [self.a, self.b, self.c, self.d, self.e]


arr = []
for i in range(10):
    arr.append(GG(randint(0, 50),
                  randint(0, 50),
                  randint(0, 50),
                  randint(0, 50),
                  randint(0, 50)))


def find_solve_1(arr):
    err = []
    for i in range(10):
        err.append(arr[i].solve_1())
    print([round(i, 2) for i in err])
    if min(err) == 0:
        print('\n', arr[err.index(min(err))].get_koef())
        quit()
    return arr[err.index(min(err))].get_koef(), min(err)


def find_solve_2(arr):
    err = []
    for i in range(10):
        err.append(arr[i].solve_2())
    print([round(i, 2) for i in err])
    if min(err) == 0.0:
        print('\n', arr[err.index(min(err))].get_koef())
        quit()
    return arr[err.index(min(err))].get_koef(), min(err)


for i in range(sys.maxsize):
    print(i, end=' ')
    koef, error = find_solve_2(arr)
    arr = []
    for k in range(10):
        arr.append(GG(randint(-1, 1) + koef[0],
                      randint(-1, 1) + koef[1],
                      randint(-1, 1) + koef[2],
                      randint(-1, 1) + koef[3],
                      randint(-1, 1) + koef[4]))


