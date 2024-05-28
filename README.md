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

The idea is to use inscribed regular polygons to approximate the circumference of the circle.

Unfortunately, this converges only very slowly. You gain only about 0.6 digits of pi for each iteration.

So, to get 1_000_000 digits, you will need 6_000_000 iterations. At that point you are using a polygon with around 5.65e1806180 sides.

The related method of using circumscribed polygons has even worse behavior.

Archimedes gave up after 5 iterations.

```
usage: archimedes.py [-h] [-i ITERATIONS]
```

## leibniz

The [Leibniz series for pi](https://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80)
is a very simple and elegant formula.

However, it is extremely slow to converge. In order to get to 10 decimal places requires
evaluation of almost 5 billion terms.

There are ways to speed up convergence.

```
usage: leibniz.py [-h] [-i ITERATIONS]
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

For all these, the number of extra digits you get for 5 times the
iterations is pretty low.
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

## machin-like-4

Same code as `machin-like` but the formula has been changed to a 4-term equation
that was used in 2002 to compute 1.2 trillion digits of pi in Japan.

You get about 3.4 digits per iteration

```
usage: machin-like-4.py [-h] [-i ITERATIONS]
```

## machin-with-shanks

Applying Shanks' Transform to a Machin like formula, should give you more
digits per iteration. This uses the same formula as `machin-like-4`

The tiny increase in converge rate doesn't make up for the extra work
done per iteration. At least for this sequence, it isn't worth it.


You get about 3.4 digits of pi per iteration

```
usage: machin-with-shanks.py [-h] [-i ITERATIONS]
```

## machin-4-mp

The individual terms of the machin-like are independent and can run
in parallel. This does just that to the `machin-like-4`.

In theory, you should get a 4x speed up.

You could go deeper and split each term into the positive and negative sub-terms,
for instance.

```
usage: machin-4-mp.py [-h] [-i ITERATIONS]
```

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
usage: chodnovsky-iter2.py [-h] [-i ITERATIONS]
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
|machin-like         |  5:17:55   | 555,555 |
|machin-like-4       |  5:09:42   | 295,334 |
|machin-with-shanks  |  5:35:27   | 294,118 |
|machin-4-mp         |  1:22:15   | 295,334 |
|chudnovsky-iter     |  0:58:09   | 100,000 |
|chudnovsky-iter2    |  0:16:06   | 100,000 |

## Things I think I've learned

### Shanks Transform is probably not worth it.
If you are computing sequences by hand, then Shanks Transform can be a life
saver.

When using a computer it doesn't pay back except for extreme cases (like leibnitz)

This is because you must cache `2+n` partial sums for `n` layers. The memory cost
and compute time for buffer management doesn't pay. Now, it might in something
like C++ with a good ring buffer implementation.

### bigfloat vs mpmath
They seem to be about the same speed - bigfloat might be a little faster.

However, I found mpmath easier to deal with. The global context in
mpmath seemed a bit "stickier" than the one in bigfloat making it easier to
make sure all calcs were done at the same precision - especially when doing
"mixed calcs" with python native number types.

### Multiprocessing in Python
Multiprocessing in Python has some sophisticated support. Setting up a simple case
is indeed simple.

## Other resources

Of course, there is some hyperfast code if you
are comfortable with C++ : [Compute billion of pi digits using GMP](https://gmplib.org/pi-with-gmp)

I checked my work for a million digits against
this list : [Million digits](https://www.piday.org/million/)

If hand calculation is more your speed, [Stand-up Maths](https://www.youtube.com/@standupmaths)
has done a whole series on that.

[Brink's paper on Nilakantha](https://www.researchgate.net/publication/283579663_Nilakantha's_accelerated_series_for_pi/link/5640d4f008ae24cd3e40afa5/download?_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uIn19)