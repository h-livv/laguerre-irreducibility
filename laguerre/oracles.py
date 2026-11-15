"""
Exact checks on a single polynomial.

Two oracles settle one pair (n, a) without using any lemma of the paper:

    1. Full factorisation over Q (SageMath). Only practical for small n.
    2. Integer-root search. The polynomial is monic up to sign, so it has a linear factor
       exactly when it has an integer root. All roots lie in (0, B] with B from Lemma 6.4.

This is the only library module that needs SageMath (for the factorisation).

The polynomial is always the scaled one:

    script-L_n^(a)(x) = sum_{j=0}^{n} (-1)^j a_j x^j,   a_j = C(n, j) (n+a)! / (j+a)!.

It has the same factor degrees as L_n^(a)(x).
"""

from math import gcd, isqrt

from sage.all import ZZ, PolynomialRing

from laguerre.arithmetic import radical, subset_sums

POLYNOMIAL_RING = PolynomialRing(ZZ, "x")

# Three (Mersenne) primes. A candidate root is first tested modulo these, which is fast.
# Only a candidate that is a root modulo all three is evaluated exactly.
CHECK_PRIMES = [2**61 - 1, 2**89 - 1, 2**107 - 1]


# ----------------------------------------------------------------------------------------
# The polynomial.
# ----------------------------------------------------------------------------------------

def laguerre_coefficients(n, a):
    """
    Return the list [a_0, a_1, ..., a_n] of the positive integers a_j = C(n, j) (n+a)!/(j+a)!.

    We start from a_n = 1 and go down with the exact recurrence

        a_{j-1} = a_j * j * (a + j) / (n - j + 1),

    which follows from C(n, j-1) / C(n, j) = j / (n - j + 1).
    """
    coefficients = [0] * (n + 1)
    coefficients[n] = 1
    for j in range(n, 0, -1):
        numerator = coefficients[j] * j * (a + j)
        denominator = n - j + 1
        assert numerator % denominator == 0
        coefficients[j - 1] = numerator // denominator
    return coefficients


def signed_laguerre_coefficients(n, a):
    """Return the list [c_0, ..., c_n] with c_j = (-1)^j a_j, the coefficient of x^j."""
    coefficients = laguerre_coefficients(n, a)
    signed = []
    for j in range(0, n + 1):
        if j % 2 == 0:
            signed.append(coefficients[j])
        else:
            signed.append(-coefficients[j])
    return signed


def laguerre_polynomial(n, a):
    """Return script-L_n^(a)(x) as a SageMath polynomial with integer coefficients."""
    return POLYNOMIAL_RING(signed_laguerre_coefficients(n, a))


# ----------------------------------------------------------------------------------------
# Oracle 1: factorisation over Q.
# ----------------------------------------------------------------------------------------

def factor_degrees(n, a):
    """
    Return the sorted list of the degrees of the irreducible factors of script-L_n^(a)(x)
    over Q, repeated according to multiplicity. An irreducible polynomial gives [n].
    """
    factorization = laguerre_polynomial(n, a).factor()
    degrees = []
    for factor, multiplicity in factorization:
        for _ in range(multiplicity):
            degrees.append(int(factor.degree()))
    return sorted(degrees)


def is_irreducible(n, a):
    """Return True if script-L_n^(a)(x) is irreducible over Q."""
    return factor_degrees(n, a) == [n]


def has_factor_of_degree(n, a, k):
    """
    Return True if script-L_n^(a)(x) has a factor of degree k over Q.

    A factor of degree k exists exactly when k is a sum of some of the degrees of the
    irreducible factors.
    """
    return k in subset_sums(factor_degrees(n, a))


# ----------------------------------------------------------------------------------------
# Oracle 2: integer roots.
# ----------------------------------------------------------------------------------------

def szego_root_bound(n, a):
    """
    Return the integer part of the bound B of Lemma 6.4 (Szego): every root x satisfies

        0 < x <= B = 2n + a + 1 + sqrt( (2n + a + 1)^2 + 1/4 - a^2 ).

    So every INTEGER root is at most the returned value. Computed exactly, without floats:
    the square root equals sqrt(M) / 2 with M = 4 ((2n+a+1)^2 - a^2) + 1.
    """
    s = 2 * n + a + 1
    M = 4 * (s * s - a * a) + 1
    return s + isqrt(M) // 2


def evaluate_polynomial(coefficients, x, modulus=None):
    """
    Evaluate the polynomial with coefficient list [c_0, ..., c_n] at the integer x by
    Horner's rule. If `modulus` is given, the result is reduced modulo it at every step.
    """
    value = 0
    for coefficient in reversed(coefficients):
        value = value * x + coefficient
        if modulus is not None:
            value = value % modulus
    return value


def find_integer_roots(n, a, candidates):
    """
    Return the list of those integers in `candidates` that are roots of script-L_n^(a)(x).

    Each candidate is tested modulo the three CHECK_PRIMES first. A true root is 0 modulo
    every prime, so no root is lost. Survivors are then confirmed with exact arithmetic.
    """
    signed = signed_laguerre_coefficients(n, a)
    reduced = []
    for prime in CHECK_PRIMES:
        reduced.append([coefficient % prime for coefficient in signed])

    roots = []
    for xi in candidates:
        is_root_modulo_all_primes = True
        for index in range(len(CHECK_PRIMES)):
            if evaluate_polynomial(reduced[index], xi, CHECK_PRIMES[index]) != 0:
                is_root_modulo_all_primes = False
                break
        if is_root_modulo_all_primes:
            if evaluate_polynomial(signed, xi) == 0:
                roots.append(xi)
    return roots


def direct_root_candidates(n, a):
    """
    Return every integer xi that could be a root, using only two facts:

        0 < xi <= B                (Lemma 6.4)
        Rad(n (n + a)) divides xi  (first lines of the proof of Proposition 1.3: n | xi^n
                                    and (n + a) | xi^n, by Lemma 2.9(i))

    This is the direct test. It does not use the rest of Proposition 1.3.
    """
    bound = szego_root_bound(n, a)
    step = radical(n * (n + a))
    return list(range(step, bound + 1, step))


def proposition_1_3_candidates(n, a):
    """
    Return every integer xi that passes ALL the necessary conditions for an integer root
    in the proof of Proposition 1.3 (needs n >= 2):

        0 < xi <= B and Rad(n (n + a)) | xi           (as in direct_root_candidates)
        d1 = gcd(xi^(n-1), n - 1),      n1 = (n - 1) / d1            (equation (19))
        d2 = gcd(xi^(n-1), n + a - 1),  n2 = (n + a - 1) / d2        (equation (19))
        xi = a + 1 (mod n1)   and   xi = -a + 1 (mod n2)             (equation (20))

    Formula (1) of the paper, xi = 2n + a - 1 + gamma (n-1)(n+a-1)/(d1 d2), and the bound
    d1 d2 > (n-1)/6 are consequences of exactly these conditions, so we do not need to
    loop over d1, d2 and gamma: we loop over xi and compute d1 and d2 from it.
    """
    candidates = []
    for xi in direct_root_candidates(n, a):
        d1 = gcd(pow(xi, n - 1, n - 1), n - 1)
        d2 = gcd(pow(xi, n - 1, n + a - 1), n + a - 1)
        n1 = (n - 1) // d1
        n2 = (n + a - 1) // d2
        if (xi - (a + 1)) % n1 != 0:
            continue
        if (xi - (-a + 1)) % n2 != 0:
            continue
        candidates.append(xi)
    return candidates
