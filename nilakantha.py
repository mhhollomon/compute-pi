#!/usr/bin/env python
import argparse
from mpmath import mpf

from lib.common import BaseCalc, driver


class calculator(BaseCalc) :
    name = 'nilakantha'
    description = 'Approximate pi using Nilakantha power series'

    digits_per_iter = 0.00001

    def __init__(self) -> None:

        # first iteration needs to be "0"
        super().__init__(first_iter=0)

        self.sign : int = -1

        self.total_sum = mpf(0)

    
    def add_term(self) :

        self.sign *= -1
        sub_n = mpf(2+2*self.k)
        denominator = sub_n *(sub_n+1) * (sub_n+2)
        new_term = mpf(self.sign) / denominator
        self.total_sum += new_term

    def final_compute(self) :
        return self.total_sum * 4 + 3
    


if __name__ == "__main__" :

    driver(calculator)

