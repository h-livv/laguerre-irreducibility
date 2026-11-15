"""
Integer helper functions, including Legendre's formula (Lemma 2.5).

Everything here is exact integer arithmetic in plain Python. Nothing depends on SageMath.

Notation of the paper (Section 2):

    nu_p(m)       the exponent of the prime p in m                       -> valuation(m, p)
    sigma_p(m)    the sum of the base-p digits of m                      -> digit_sum(m, p)
    P(m)          the largest prime factor of m, with P(1) = 1           -> largest_prime_factor(m)
    Rad(m)        the product of the distinct primes dividing m          -> radical(m)
    omega_p(m)    the number of distinct primes q >= p dividing m        -> omega_from(m, p)
    Delta(m, l)   the product m (m+1) ... (m+l-1) of l consecutive ints  -> delta(m, l)

Functions whose name ends in "_of_delta" answer the same question for Delta(m, l) without
ever multiplying the l numbers together.
"""

from functools import lru_cache


# ----------------------------------------------------------------------------------------
# Primes and factorisation (trial division; all our numbers are small enough).
# ----------------------------------------------------------------------------------------

def is_prime(m):
    """Return True if m is a prime number."""
    if m < 2:
        return False
    divisor = 2
    while divisor * divisor <= m:
        if m % divisor == 0:
            return False
        divisor += 1
    return True


def primes_up_to(limit):
    """Return the sorted list of all primes p <= limit."""
    return [m for m in range(2, limit + 1) if is_prime(m)]


@lru_cache(maxsize=None)
def prime_factorization(m):
    """
    Return the prime factorisation of m >= 1 as a tuple of (prime, exponent) pairs,
    sorted by prime. Example: prime_factorization(360) == ((2, 3), (3, 2), (5, 1)).

    The results are memoised, because the same numbers are factorised many times.
    """
    if m < 1:
        raise ValueError("prime_factorization needs m >= 1")
    factors = []
    remaining = m
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            exponent = 0
            while remaining % divisor == 0:
                remaining //= divisor
                exponent += 1
            factors.append((divisor, exponent))
        divisor += 1
    if remaining > 1:
        factors.append((remaining, 1))
    return tuple(factors)


def prime_divisors(m):
    """Return the sorted list of the distinct primes dividing m >= 1."""
    return [prime for prime, exponent in prime_factorization(m)]


def largest_prime_factor(m):
    """P(m): the largest prime factor of m, with the convention P(1) = 1."""
    primes = prime_divisors(m)
    if len(primes) == 0:
        return 1
    return primes[-1]


def radical(m):
    """Rad(m): the product of the distinct primes dividing m."""
    product = 1
    for prime in prime_divisors(m):
        product *= prime
    return product


def omega_from(m, p):
    """omega_p(m): the number of distinct primes q >= p that divide m. (Equation (2).)"""
    return len([q for q in prime_divisors(m) if q >= p])


def divisors(m):
    """Return the sorted list of all positive divisors of m >= 1."""
    result = [1]
    for prime, exponent in prime_factorization(m):
        new_result = []
        for divisor in result:
            for power in range(exponent + 1):
                new_result.append(divisor * prime**power)
        result = new_result
    return sorted(result)


# ----------------------------------------------------------------------------------------
# p-adic valuations. Lemma 2.5 (Legendre) gives the valuation of a factorial.
# ----------------------------------------------------------------------------------------

def valuation(m, p):
    """nu_p(m): the largest e with p^e dividing m. Needs m != 0."""
    if m == 0:
        raise ValueError("nu_p(0) is infinite")
    remaining = abs(m)
    exponent = 0
    while remaining % p == 0:
        remaining //= p
        exponent += 1
    return exponent


def digit_sum(m, p):
    """sigma_p(m): the sum of the digits of m >= 0 written in base p."""
    total = 0
    remaining = m
    while remaining > 0:
        total += remaining % p
        remaining //= p
    return total


def factorial_valuation(m, p):
    """
    nu_p(m!) by Legendre's formula (Lemma 2.5):

        nu_p(m!) = (m - sigma_p(m)) / (p - 1).

    The factorial itself is never computed.
    """
    return (m - digit_sum(m, p)) // (p - 1)


def binomial_valuation(n, j, p):
    """nu_p of the binomial coefficient C(n, j), for 0 <= j <= n."""
    return factorial_valuation(n, p) - factorial_valuation(j, p) - factorial_valuation(n - j, p)


# ----------------------------------------------------------------------------------------
# Delta(m, l) = m (m+1) ... (m+l-1), a product of l consecutive integers starting at m.
# ----------------------------------------------------------------------------------------

def delta(m, l):
    """Delta(m, l) = m (m+1) ... (m+l-1). Only use this for small l."""
    product = 1
    for term in range(m, m + l):
        product *= term
    return product


def delta_valuation(m, l, p):
    """nu_p(Delta(m, l)) for m >= 1, computed as nu_p((m+l-1)!) - nu_p((m-1)!)."""
    return factorial_valuation(m + l - 1, p) - factorial_valuation(m - 1, p)


def prime_divisors_of_delta(m, l):
    """Return the sorted list of the distinct primes dividing Delta(m, l), for m >= 1."""
    primes = set()
    for term in range(m, m + l):
        for prime in prime_divisors(term):
            primes.add(prime)
    return sorted(primes)


def largest_prime_factor_of_delta(m, l):
    """P(Delta(m, l)), with the convention P(1) = 1."""
    primes = prime_divisors_of_delta(m, l)
    if len(primes) == 0:
        return 1
    return primes[-1]


def omega_from_of_delta(m, l, p):
    """omega_p(Delta(m, l)): the number of distinct primes q >= p dividing Delta(m, l)."""
    return len([q for q in prime_divisors_of_delta(m, l) if q >= p])


# ----------------------------------------------------------------------------------------
# Small utilities.
# ----------------------------------------------------------------------------------------

def is_perfect_square(m):
    """Return True if m >= 0 is the square of an integer."""
    root = 0
    while root * root < m:
        root += 1
    return root * root == m


def is_perfect_cube(m):
    """Return True if m >= 0 is the cube of an integer."""
    root = 0
    while root * root * root < m:
        root += 1
    return root * root * root == m


def subset_sums(widths):
    """
    Return the set of all sums of sub-collections of the list `widths` (the empty sum 0
    is included). Used for Dumas' theorem and for reading factor degrees.
    """
    sums = {0}
    for width in widths:
        new_sums = set(sums)
        for value in sums:
            new_sums.add(value + width)
        sums = new_sums
    return sums


# ----------------------------------------------------------------------------------------
# The quantities defined at the start of Section 4 of the paper.
# ----------------------------------------------------------------------------------------

def section4_quantities(n, a, k, p):
    """
    Return the quantities l, u0, j0, v0, t0, t1, c0 of Section 4, as a dictionary.

    The prime p must divide Delta(n-k+1, k) = (n-k+1) ... (n-1) n. Then:

        l, u0   0 <= l <= k-1 with p | (n - l), and u0 = nu_p(n - l) >= 1.
                (If several l qualify, which needs p < k, we return the smallest one.
                 The lemmas of the paper only use p > k, where l is unique.)
        j0, v0  the unique 1 <= j0 <= p with p | (a + j0), and v0 = nu_p(a + j0) >= 1.
        t0      (a + j0) / p^v0, which is not divisible by p.
        t1      the unique 1 <= t1 < p with t0 + t1 = 0 (mod p).
        c0      the least positive integer with a + p + p^2 <= (p - 1) p^c0.   (Equation (6).)
    """
    l = None
    for candidate in range(0, k):
        if (n - candidate) % p == 0:
            l = candidate
            break
    if l is None:
        raise ValueError("p = %d does not divide Delta(n-k+1, k) for n = %d, k = %d" % (p, n, k))
    u0 = valuation(n - l, p)

    j0 = None
    for candidate in range(1, p + 1):
        if (a + candidate) % p == 0:
            j0 = candidate
            break
    v0 = valuation(a + j0, p)

    t0 = (a + j0) // p**v0
    t1 = (-t0) % p

    c0 = 1
    while a + p + p * p > (p - 1) * p**c0:
        c0 += 1

    return {"l": l, "u0": u0, "j0": j0, "v0": v0, "t0": t0, "t1": t1, "c0": c0}
