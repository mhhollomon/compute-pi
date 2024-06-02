#!/usr/bin/env python
import argparse
import datetime
from mpmath import mp, mpf

from lib.common import BaseCalc, driver

from typing import List, NamedTuple

from multiprocessing import Pool

import functools

Params = NamedTuple('Params', factor=int, base=int)

class MachinTerm :
    def __init__(self, factor, argument) -> None:
        self.factor = factor
        self.argument = argument
 
        self.power = argument
        self.partial = argument

        self.arg_squared = argument**2
        self.sign : int = 1
        self.k : int = 0
        self.divisor = mpf(1)

    def compute_term(self) :
        self.k += 1
        self.sign *= -1
        self.divisor += 2

        self.power *= self.arg_squared

        new_term = self.power * self.sign / self.divisor
        self.partial += new_term



Parameters = [
    Params(12, 49),
    Params(32, 57),
    Params(-5, 239),
    Params(12, 110443)
]

class machin(BaseCalc) :
    name = 'machin-4-mp'
    description = 'Approximate pi using a "Machin-like" arctan formula with 4 terms'
    
    digits_per_iter = 3.369

    def __init__(self) -> None:
        super().__init__()

        self.params = [MachinTerm(
            factor = mpf(p.factor), 
            argument = mpf(1) / p.base,
            ) for p in Parameters]

    def do_machin_term(self, index : int ) :
        t : MachinTerm = self.params[index]

        start_time = datetime.datetime.now()

        for i in range(0, self.iterations) :
            t.compute_term()
            if index == 0 and i % self.progress_count == 0 :
                print(f"{i:6} {datetime.datetime.now() - start_time}")

        return t.partial * t.factor

    def approx_pi(self) :
        with Pool(5) as p:
            retvals = p.map(self.do_machin_term, range(0, len(self.params)))

        func = lambda a,b : a+b
        pi = mpf(4) * functools.reduce(func, retvals)

        return pi
    

if __name__ == "__main__" :

    driver(machin)

