#!/usr/bin/env python
from mpmath import mpf

from typing import NamedTuple

from lib.common import BaseCalc, driver


Params = NamedTuple('Params', factor=int, base=int)

#
# Each branch of a machin-like formula looks like a * arctan(b)
# factor = a
# argument = b
# This class will compute the partial sums for the arctan.
#
class MachinTerm :
    def __init__(self, factor, argument) -> None:
        super().__init__()

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
# This particular set whas used in 2002 to set a world
# record on the numbr of digits.
#
Parameters = [
    Params(12, 49),
    Params(32, 57),
    Params(-5, 239),
    Params(12, 110443)
]

class machin(BaseCalc) :
    name = 'machin-like-4'
    description = 'Approximate pi using a "Machin-like" arctan formula with 4 terms'

    digits_per_iter = 3.369

    def __init__(self) -> None:
        super().__init__()

        self.params = [MachinTerm(
            factor = mpf(p.factor), 
            argument = mpf(1) / p.base,
            ) for p in Parameters]

    def add_term(self) -> None :
        """Give each branch of the formula a chance to add another term to 
        their arctan partial sum"""

        for t in self.params :
            t.compute_term()

    def final_compute(self) :
        total = mpf(0) 
        for t in self.params :
            total += t.partial * t.factor

        return total * 4



if __name__ == "__main__" :

    driver(machin)

