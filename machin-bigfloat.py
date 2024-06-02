#!/usr/bin/env python
import argparse
import datetime

from bigfloat import BigFloat, setcontext, Context, pow, div, mul

from typing import NamedTuple
name = 'machin-bigfloat'
description = 'Approximate pi using a "Machin-like" arctan formula'
digits_per_iter = 1.84
count_between_progress = 500

Params = NamedTuple('Params', factor=int, base=int)

class MachinTerm :
    def __init__(self, factor, argument) -> None:
        self.factor = factor
        self.argument = argument
        self.partial = argument
        self.power = argument

        self.arg_squared = pow(argument, 2)

        self.sign : int = 1
        self.k : int = 0
        self.divisor = BigFloat(1)

    def compute_term(self) :
        self.k += 1
        self.sign *= -1
        self.divisor += 2

        self.power *= self.arg_squared
        new_term = div(mul(self.power, self.sign), self.divisor)
        self.partial += new_term



Parameters = [
    Params(6, 8),
    Params(2, 57),
    Params(1, 239)
]

class machin :
    def __init__(self) -> None:
        self.k = 0

        self.params = [MachinTerm(
            factor = BigFloat(p.factor), 
            argument = div(BigFloat(1), p.base),
            ) for p in Parameters]

    
    def add_term(self) :
        self.k += 1

        for t in self.params :
            t.compute_term()

    def approx_pi(self) -> BigFloat :
        total = BigFloat(0) 
        for t in self.params :
            total += t.partial * t.factor

        return total * 4
    

def main(iterations : int = 100) :

    dps = int(iterations * digits_per_iter * 1.1)
    if dps < 1000 :
        dps = 1000

    # bigfloat precision is in bits
    setcontext(Context(precision=int(1+3.333*dps)))

    C = machin()

    start_time = datetime.datetime.now()

    for i in range(0, iterations) :
        C.add_term()
        k = C.k
        if k % count_between_progress == 0 :
            delta = datetime.datetime.now() - start_time
            print(f"{k:6} of {iterations} ({delta})")


    pi = C.approx_pi()
    bits = pi.precision
    precision = int(bits / 3.333)

    index = int(iterations*digits_per_iter + 2)
    if index < 52 :
        index = 52
    pi_str : str = str(pi)[:index]
    print(">> Index =", index)
    print(">> len =", len(pi_str))

    places : int = 12
    start : int = 0
    n : int = 0
    col_count : int = 10
    first : bool = True

    while(start < len(pi_str)) :
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

        
        print(f"{prefix}{pi_str[start : start+places]}", end="")
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

    print(f"{name} - prec = {precision} ({dps}, {bits})")
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

