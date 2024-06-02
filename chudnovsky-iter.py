#!/usr/bin/env python
from mpmath import mp, mpf

from lib.common import BaseCalc, driver

class calculator(BaseCalc) :
    name = 'chudnovsky-iter'
    description = 'Approximate pi using a chudnovsky formula'
    digits_per_iter = 10

    def __init__(self) -> None:
        super().__init__()

        self.k_fact_to_third = mpf(1)
        self.three_k_fact = mpf(1)
        self.six_k_fact = mpf(1)
        self.top_sum = mpf('13591409')
        self.bottom_power = mpf(1)

        self.sign : int = 1
        self.front_factor = mpf(1) / (mpf(426880) * mp.sqrt(mpf(10005)))
        self.top_sum_a = mpf('545140134')
        self.bottom_base = mpf('640320')

        self.total_sum = self.six_k_fact * self.top_sum / \
            (self.three_k_fact * self.k_fact_to_third * self.bottom_power)

    def add_term(self) :
        self.k_fact_to_third *= mp.power(self.k, 3)

        three = 3 * self.k
        for i in range(three-2, three+1) :
            self.three_k_fact *= mpf(i)

        six = 6 * self.k
        for i in range(six-5, six+1) :
            self.six_k_fact *= mpf(i)
        
        self.top_sum += self.top_sum_a

        self.bottom_power *= mp.power(self.bottom_base, 3)

        self.sign *= -1

        new_term = mpf(self.sign) * self.six_k_fact * self.top_sum / \
            (self.three_k_fact * self.k_fact_to_third * self.bottom_power)
        
        self.total_sum += new_term

    def final_compute(self) :
        one_over = self.total_sum * self.front_factor
        pi = mpf(1) / one_over
        return pi
    


if __name__ == "__main__" :

    driver(calculator)

