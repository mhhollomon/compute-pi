#!/usr/bin/env python
import argparse
import datetime
from mpmath import mp, mpf

class calculator :
    def __init__(self) -> None:
        self.k = 0
        self.k_fact_to_third = mpf(1)
        self.three_k_fact = mpf(1)
        self.six_k_fact = mpf(1)
        self.top_sum = mpf('13591409')
        self.bottom_power = mpf(1)

        self.front_factor = mpf(1) / (mpf(426880) * mp.sqrt(mpf(10005)))
        self.top_sum_a = mpf('545140134')
        self.bottom_base = mpf('640320')

        self.total_sum = self.six_k_fact * self.top_sum / \
            (self.three_k_fact * self.k_fact_to_third * self.bottom_power)

    def add_term(self) :
        self.k += 1

        self.k_fact_to_third *= mp.power(self.k, 3)

        three = 3 * self.k
        for i in range(three-2, three+1) :
            self.three_k_fact *= mpf(i)

        six = 6 * self.k
        for i in range(six-5, six+1) :
            self.six_k_fact *= mpf(i)
        
        self.top_sum += self.top_sum_a

        self.bottom_power *= mp.power(self.bottom_base, 3)

        sign = 1 if self.k % 2 == 0 else -1


        new_term = mpf(sign) * self.six_k_fact * self.top_sum / \
            (self.three_k_fact * self.k_fact_to_third * self.bottom_power)
        
        self.total_sum += new_term

    def approx_pi(self) :
        one_over = self.total_sum * self.front_factor

        return mpf(1) / one_over
    

def main(iterations : int = 100) :

    dps = int(iterations * 10.5)
    if dps < 1000 :
        dps = 1000

    mp.dps = dps

    C = calculator()

    start_time = datetime.datetime.now()

    for i in range(0, iterations) :
        C.add_term()
        k = C.k
        if k % 100 == 0 :
            delta = datetime.datetime.now() - start_time
            print(f"{k:6} of {iterations} ({delta})")


    index = iterations*10 +2
    if index < 52 :
        index = 52
    pi : str = str(C.approx_pi())[:index]

    places : int = 12
    start : int = 0
    n : int = 0
    col_count : int = 10
    first : bool = True

    while(start < len(pi)) :
        if col_count == 10 :
            print(f"{n:6}|", end="")

        # For the first line, no prefix to make room for '3.'
        # For the start of every other line two spaces
        # Between other groups, one space
        if first :
            prefix = ""
            first = False
        elif col_count == 10 :
            prefix = "  "
        else :
            prefix = " "

        
        print(f"{prefix}{pi[start : start+places]}", end="")
        start += places
        places = 10
        n += 1
        col_count -= 1
        if col_count < 1 :
            print()
            col_count = 10
        
    # we printed less than a full line
    if col_count < 10 :
        print()

#--------------------------------------------
def get_args() :
    parser = argparse.ArgumentParser(
                    prog='chodnovsk-iter.py',
                    description='Approximate pi using an iterative form of the Chudnovsky algorithm',
    )

    parser.add_argument("-i", '--iterations', type=int, default=100)

    return parser.parse_args()

if __name__ == "__main__" :

    args = get_args()

    main(args.iterations)

