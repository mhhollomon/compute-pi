# compute-pi
Various attempts to compute pi in python.

*NOTE* - all of these are very naive implementations of the algorthim and
are intended more as learning aids and demos than serious attempts at speed.

## Set up
You will definitely want to make sure you install [GMP](https://gmplib.org/)
first.

While not strictly necessary (mpmath will work without it), it is so slow as to be pointless.

If you are on Debian you can do this as

```
sudo apt install libgmp-dev
```

Then you set up a python virtual environment

```
python -m venv .venv
source .venv/bin/activate
pip install gmpy mpmath
```
## archimedes

Use the same algorithm that Archimedes did to hand calculate. [This video](https://www.youtube.com/watch?v=_rJdkhlWZVQ) gives a good overview.

The idea is use inscribed regular polygons to approximate the circumference of
the circle.

Unfortunately, this converges only very slowly. You gain only about 0.6 digits of pi
for each iteration.

So, to get 1_000_000 digits, you will need 6_000_000 iterations. At that point you
are using a polygon with around 5.65e1806180 sides.

The related method of using circumscribed polygons has silghtly worse behavior.

Archimedes gave up after 4 iterations.

```
usage: archimedes.py [-h] [-i ITERATIONS]
```

## leibniz

The [Leibniz series for pi](https://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80)
is a very simple and elegant formula.

However, it is extremely slow to converge. In order to get to 10 decimal places requires
evalutaion of almost 5 billion terms.

There are ways to speed up convergence.

```
usage: liebniz.py [-h] [-i ITERATIONS]
```

## shanks

Use [Shanks' Transform](https://en.wikipedia.org/wiki/Shanks_transformation) to speed
up the Leibniz series.

I feel that I might have the code wrong for this. But see what you think.

You can actually apply the transform multiple times.

You get this many digits based on the layers :
|layers|digits @ 2000| digits @ 10000 |
| -- | -- | -- |
| 0 |  2 |  3 |
| 1 |  9 | 10 |
| 2 | 16 | 20 |
| 3 | 23 | 27 |
| 4 | 28 | 36 |
| 5 | 36 | 43 |
| 100 | 281 | 482 |

For all these, the number of extra digits you get for 5 times the iterations is
pretty low.

```
usage: shanks.py [-h] [-i ITERATIONS] [-l LAYERS]
```
## machin-like

Recognizing that the Leibnitz formula is the Gregory's series expansion for arctan evaluated
at 1, [John Machin](https://en.m.wikipedia.org/wiki/John_Machin) came up with
a formula that used multiple arctans to increase the rate of convergence.

I used a "Machin-like" formula used in 1961 to compute 100,000 digits of pi on an
IBM 7090.

You get about 1.8 digits of pi per iteration.
```
usage: machin-like.py [-h] [-i ITERATIONS]
```

## machin-with-shanks

Applying Shanks' Transform to a Machin like formula, should give you more
digits per iteration.

I also changed the machin-like to use one that was used in 2002 to compute 
1.2 trillion digits of pi.

You get about 3.4 digits of pi per iteration

```
usage: machin-with-shanks.py [-h] [-i ITERATIONS]
```

## machin-shanks-mp

The individual terms of the machin-like are independent and can run
in parallel. This does just that.

In theory, you should get a 4x speed up.

## chudnovsky-iter

A simple minded iterative version of the [Chudnovsky Algorithm](https://en.wikipedia.org/wiki/Chudnovsky_algorithm).

Because it is iterative, it cannot use multitasking. 
Even so, I was able to compute 200,000 digits of pi in about 6 minutes.

```
usage: chodnovsk-iter.py [-h] [-i ITERATIONS]
```

Note that you get about 10 digits of pi for every iteration.

The algorithm slows down as more and more iterations are done. 

## chudnovsky-iter2

A slightly more efficient iterative version of the 
[Chudnovsky Algorithm](https://en.wikipedia.org/wiki/Chudnovsky_algorithm).


```
usage: chodnovsk-iter2.py [-h] [-i ITERATIONS]
```

Note that you get about 10 digits of pi for every iteration.

This does __NOT__ slow down in the later iterations and it makes
a significant difference in the time taken.

## Timings

Time and iterations needed to get 1_000_000 digits of pi for each algorithm.

If there is a star in the algorithm box, I was not able to finish the calculation.
The timing column contains an approximation of how long it would take based
on what I could do.

| Algorithm | Timing | iterations |
| ---                | ---     | --- |
|archimedes        * |  500 hours | 6,000,000 |
|leibnitz          * |  ?         | 5E100000 (ish) |
|shanks            * |  ?         | 44,000,000 with 100 layers |
|machin-like       * |  5:16:00   | 555,555 |
|machin-with-shanks *|  5:00:00   | 294,118 |
|machin-shanks-mp    |            | 294,118 |
|chudnovsky-iter     |  0:58:09   | 100,000 |
|chudnovsky-iter2    |  0:16:06   | 100,000 |

## Other resources

Of course, there is some hyperfast code if you
are comfortable with C++ : [Compute billion of pi digits using GMP](https://gmplib.org/pi-with-gmp)

I checked my work for a million digits against
this list : [Million digits](https://www.piday.org/million/)

If hand calculation is more your speed, [Stand-up Maths](https://www.youtube.com/@standupmaths)
has done a whole series on that.

