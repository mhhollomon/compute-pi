#!/usr/bin/env python
from mpmath import mpf

from lib.common import BaseCalc, driver


class calculator(BaseCalc) :
    name = 'euler'
    description = 'Approximate pi using euler transform power series'

    digits_per_iter = .30

    def __init__(self) -> None:
        super().__init__(first_iter=1)

        # pull of the first term (k=0) so we don't
        # have to deal with things like 0!
        self.total_sum = mpf(2)
        self.k_fact = mpf(1)
        self.two_power = mpf(2)
        self.denom_fact = mpf(1)

    
    def add_term(self) :

        self.k_fact *= self.k
        self.denom_fact *= (2 * self.k) * (2* self.k + 1)
        self.two_power *= 2

        new_term = (self.two_power * self.k_fact * self.k_fact) / self.denom_fact
        self.total_sum += new_term

    def final_compute(self) :
        return self.total_sum
        


if __name__ == "__main__" :

    driver(calculator)

