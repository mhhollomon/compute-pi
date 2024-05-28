#!/usr/bin/env python
import argparse
import datetime
from mpmath import mp, mpf

from typing import List, NamedTuple

from multiprocessing import Pool

import functools

name = 'machin-4-mp'
description = 'Approximate pi using a "Machin-like" arctan formula with 4 terms'
digits_per_iter = 3.39
count_between_progress = 500

Params = NamedTuple('Params', factor=int, base=int)

class MachinTerm :
    def __init__(self, factor, argument) -> None:
        self.factor = factor
        self.argument = argument
 
        self.power = argument
        self.partial = argument

        self.sign : int = 1
        self.k : int = 0
        self.divisor = mpf(1)

    def compute_term(self) :
        self.k += 1
        self.sign *= -1
        self.divisor += 2

        self.power *= self.argument**2

        new_term = self.power * self.sign / self.divisor
        self.partial += new_term



Parameters = [
    Params(12, 49),
    Params(32, 57),
    Params(-5, 239),
    Params(12, 110443)
]

class machin :
    def __init__(self, iterations : int) -> None:
        self.k = 0

        self.iterations = iterations

        self.params = [MachinTerm(
            factor = mpf(p.factor), 
            argument = mpf(1) / p.base,
            ) for p in Parameters]

    def do_machin_term(self, index : int ) :
        t : MachinTerm = self.params[index]

        start_time = datetime.datetime.now()

        for i in range(0, self.iterations) :
            t.compute_term()
            if index == 0 and i % count_between_progress == 0 :
                print(f"{i:6} {datetime.datetime.now() - start_time}")

        return t.partial * t.factor

    def approx_pi(self) :
        with Pool(5) as p:
            retvals = p.map(self.do_machin_term, range(0, len(self.params)))

        func = lambda a,b : a+b
        pi = mpf(4) * functools.reduce(func, retvals)

        return pi
    

def main(iterations : int = 100) :

    dps = int(iterations * digits_per_iter) + 20
    if dps < 1000 :
        dps = 1000

    mp.dps = dps

    C = machin(iterations)

    start_time = datetime.datetime.now()

    pi = C.approx_pi()

    precision = pi.context.dps

    index = int(iterations*digits_per_iter + 2)
    if index < 52 :
        index = 52
    pi_str : str = str(pi)[:index]

    print_digit_string(pi_str)

    print(f"{name} iter = {iterations} prec = {precision} ({dps})")
    print(f"total time = {datetime.datetime.now() - start_time}")

#--------------------------------------------
#
# Split digits into groups of 10 and then print
# 10 such groups on a line prefixed with a group counter
#
def print_digit_string(digits: str) :
    # number of digits per group
    dpg : int = 10
    # number of groups per line
    gpl : int = 10

    leading : str = ''
    trailing : str = ''
    [leading, trailing] = digits.split('.', 2)

    prefix : str = ' ' * (len(leading)+1)

    groups : List[str] = [trailing[start:start+dpg] for start in range(0, len(trailing), dpg)]

    n : int = 0
    groups[0] = f"{n:6}|" + leading + '.' + groups[0]
    for i in range(gpl, len(groups), gpl) :
        n += gpl
        groups[i] = f"{n:6}|" + prefix + groups[i]

    for i in range(0, len(groups), gpl) :
        print(" ".join(groups[i:i+10]))

#--------------------------------------------
def get_args() :
    parser = argparse.ArgumentParser(
                    prog=f"{name}.py",
                    description=description,
    )

    parser.add_argument("-i", '--iterations', type=int, default=100)

    return parser.parse_args()

if __name__ == "__main__" :

    args = get_args()

    main(args.iterations)

