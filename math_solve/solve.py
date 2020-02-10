"""
a + 2b + 3c + 4d + 5e = 50
Can u find solve?
"""


import numpy as np
from random import randint


class GG(object):
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def solve(self):
        return abs((self.a + 2*self.b + 3*self.c + 4*self.d + 5*self.e) - 50)

    def get_koef(self):
        return [self.a, self.b, self.c, self.d, self.e]


arr = []
for i in range(10):
    arr.append(GG(randint(0, 50),
                  randint(0, 50),
                  randint(0, 50),
                  randint(0, 50),
                  randint(0, 50)))


def find_solve(arr):
    err = []
    for i in range(10):
        err.append(arr[i].solve())
    print([round(i, 2) for i in err])
    if min(err) == 0:
        print('\n', arr[err.index(min(err))].get_koef())
        quit()
    return arr[err.index(min(err))].get_koef(), min(err)


for i in range(10000):
    koef, error = find_solve(arr)
    arr = []
    for k in range(10):
        arr.append(GG(randint(-1, 1) + koef[0],
                      randint(-1, 1) + koef[1],
                      randint(-1, 1) + koef[2],
                      randint(-1, 1) + koef[3],
                      randint(-1, 1) + koef[4]))


