#!/usr/bin/env python
import argparse
import datetime
from mpmath import mp, mpf, workdps

from typing import NamedTuple
from dataclasses import dataclass
name = 'machin-with-shanks'
description = 'Approximate pi using a "Machin-like" arctan formula helped with shanks` transfrom'
digits_per_iter = 3.4
count_between_progress = 500

Params = NamedTuple('Params', factor=int, base=int)

class MachinInfo :
    def __init__(self, factor, base, power, partial) -> None:
        self.factor = factor
        self.base = base
        self.power = power
        self.partial = partial
        self.nextterm = mpf(0)
        self.nextnextterm = mpf(0)

    def __str__(self) -> str:
        with workdps(10) :
            return f"MachineInfo[power={self.power}, partial={self.partial}, n={self.nextterm}, nn={self.nextnextterm} ]"

Parameters = [
    Params(12, 49),
    Params(32, 57),
    Params(-5, 239),
    Params(12,110443)
]

class machin :
    def __init__(self) -> None:
        self.k = 0

        self.divisor = mpf(1)

        self.params = [MachinInfo(
            factor = mpf(p.factor), 
            base = mpf(1) / p.base,
            power = mpf(1) / p.base,
            partial = mpf(1) / p.base
            ) for p in Parameters]

    
    def add_term(self) :
        self.k += 1
        self.divisor += 2

        for t in self.params :
            t.power *=  t.base**2
            sign = 1 if self.k % 2 == 0 else -1
            new_term = t.power * sign / self.divisor
            #print(f"new_term = {new_term}")

            if self.k == 1 :
                t.nextterm = new_term
            elif self.k == 2 :
                t.nextnextterm = new_term
            else :
                t.partial += t.nextterm
                t.nextterm = t.nextnextterm
                t.nextnextterm = new_term


    def compute_shank(self, m : MachinInfo) :
        # print(f">>>> {m}")
        n_plus_1 = m.partial + m.nextterm + m.nextnextterm

        shank = n_plus_1 + (m.nextnextterm**2 / (m.nextnextterm -m.nextterm))
        return shank * m.factor
        

    def approx_pi(self) :
        total = mpf(0) 
        for t in self.params :
            total += self.compute_shank(t)

        return total * 4
    

def main(iterations : int = 100) :

    dps = int(iterations * digits_per_iter * 1.1)
    if dps < 1000 :
        dps = 1000

    mp.dps = dps

    C = machin()

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

