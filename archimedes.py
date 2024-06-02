#!/usr/bin/env python
import argparse
from mpmath import mp, mpf

from lib.common import BaseCalc, driver


class calculator(BaseCalc) :
    name = 'archimedes'
    description = 'Approximate pi using inscribed polygons with an increasing number of sides'

    digits_per_iter : float = 0.6

    def __init__(self) -> None:
        """A hexagon inscribe in a unit circle will have side lengh of 1"""
        super().__init__()
        self.sides = mpf(6)

        self.side_length = mpf(1)

        self.diameter = mpf(2)
    
    def add_term(self) :
        """Use pythagorean theorem twice to figure out the length of the sides
        if you double the number of sides"""

        f = (self.side_length / 2.0)**2
        b = 1 - mp.sqrt(1 - f)
        new_len = mp.sqrt(b**2 + f)

        self.side_length = new_len
        self.sides *= 2

    def final_compute(self) :
        return (self.sides * self.side_length) / self.diameter
    

#--------------------------------------------

if __name__ == "__main__" :
    driver(calculator)

