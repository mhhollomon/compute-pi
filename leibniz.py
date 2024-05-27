#!/usr/bin/env python
import argparse
import datetime
from mpmath import mp, mpf

name = 'leibniz'
description = 'Approximate pi using Leibniz` power series'
digits_per_iter = 0.001
count_between_progress = 500

class calculator :
    def __init__(self) -> None:
        self.k = 0

        self.n = mpf(1)

        self.total_sum = mpf(1)

    
    def add_term(self) :
        self.k += 1
        self.n += 2

        new_term = mpf(1) / (self.n)

        sign = -1 if self.k % 2 == 1 else 1

        self.total_sum += new_term * sign

    def approx_pi(self) :
        return self.total_sum * 4
    

def main(iterations : int = 100) :

    dps = int(iterations * digits_per_iter * 1.1)
    if dps < 1000 :
        dps = 1000

    mp.dps = dps

    C = calculator()

    start_time = datetime.datetime.now()

    for i in range(0, iterations) :
        C.add_term()
        k = C.k
        if k % count_between_progress == 0 :
            delta = datetime.datetime.now() - start_time
            print(f"{k:6} of {iterations} ({delta})")


    index = int(iterations*digits_per_iter + 2)
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

    print(f"total time = {datetime.datetime.now() - start_time}")
        
#--------------------------------------------
def get_args() :
    parser = argparse.ArgumentParser(
                    prog=f"{name}.py",
                    description=description,
    )

    parser.add_argument("-i", '--iterations', type=int, default=100)

    return parser.parse_args()

if __name__ == "__main__" :

    args = get_args()

    main(args.iterations)

