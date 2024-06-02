#!/usr/bin/env python
import argparse
from mpmath import mpf

from lib.common import BaseCalc, driver


class calculator(BaseCalc) :
    name = 'leibniz'
    description = 'Approximate pi using Leibniz power series'

    digits_per_iter = 0.00001

    def __init__(self) -> None:
        super().__init__()
        self.n = mpf(1)
        self.sign : int = 1
        self.total_sum = mpf(1)

    
    def add_term(self) :
        self.n += 2

        new_term = mpf(1) / (self.n)

        self.sign *= -1

        self.total_sum += new_term * self.sign

    def final_compute(self) :
        return self.total_sum * 4
    


if __name__ == "__main__" :

    driver(calculator)

