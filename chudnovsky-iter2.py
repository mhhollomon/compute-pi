#!/usr/bin/env python
from mpmath import mp, mpf

from lib.common import BaseCalc, driver

class calculator(BaseCalc) :
    name = 'chudnovsky-iter'
    description = 'Approximate pi using a chudnovsky formula'
    digits_per_iter = 10

    def __init__(self) -> None:
        super().__init__()

        self.front_factor = mpf(1) / (mpf(426880) * mp.sqrt('10005'))

        self.back_sum = mpf('13591409')
        self.back_sum_a = mpf('545140134')

        self.bottom_factor = mpf('10939058860032000')

        self.total_multiplicand = mpf(1)

        # f(0)
        self.total_sum = mpf('13591409')

    def compute_next_multiplicand(self, j : int) :
        j_mp = mpf(j)

        return -(j_mp * 6.0 - 1.0) * ( j_mp*2.0 - 1.0) *( j_mp * 6.0 - 5.0) / \
                (self.bottom_factor * mp.power(j_mp, 3))
    
    
    def add_term(self) :
        self.total_multiplicand *= self.compute_next_multiplicand(self.k)
        self.back_sum += self.back_sum_a

        new_term = self.total_multiplicand * self.back_sum
        
        self.total_sum += new_term

    def final_compute(self) :
        return mpf(1) / (self.total_sum * self.front_factor)
    

if __name__ == "__main__" :
    driver(calculator)
