#!/usr/bin/env python

from mpmath import mpf
from lib.common import BaseCalc, driver

from typing import NamedTuple


Params = NamedTuple('Params', factor=int, base=int)

#
# Each branch of a machin-like formula looks like a * arctan(b)
# factor = a
# argument = b
# This class will compute the partial sums for the arctan.
#
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


#
# Store the argument for the arctan inverted.
# if it is a*arctan(1/b) store (a,b)
#
Parameters = [
    Params(6, 8),
    Params(2, 57),
    Params(1, 239)
]

class machin(BaseCalc) :
    name = 'machin-like'
    description = 'Approximate pi using a "Machin-like" arctan formula'
    
    digits_per_iter = 1.84

    def __init__(self) -> None:

        self.params = [MachinTerm(
            factor = mpf(p.factor), 
            argument = mpf(1) / p.base,
            ) for p in Parameters]

    
    def add_term(self) :

        for t in self.params :
            t.compute_term()

    def final_compute(self) :
        total = mpf(0) 
        for t in self.params :
            total += t.partial * t.factor

        return total * 4
    


if __name__ == "__main__" :

    driver(machin)

