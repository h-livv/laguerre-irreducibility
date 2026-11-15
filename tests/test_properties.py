"""
STEP 10. Property tests for Lemmas 2.4, 2.5, 2.9, 4.1, 4.2, 4.3, 6.2, 6.4 and Proposition 1.3.

A property test checks the conclusion of a lemma on many random inputs. It is NOT a proof.
Its purpose is to catch a misreading of the paper or a typo in our code.

HOW LEMMAS 4.1, 4.2 AND 4.3 ARE TESTED. These lemmas start with "suppose the polynomial has
a factor of degree k". In our range that almost never happens, so a direct test would be
empty. But their proofs use this hypothesis only through the Newton polygon of the SAME
prime p (Lemmas 2.7 and 2.8). So we test the slightly stronger statement

    "if k is in the Dumas degree set D_p(n, a), then the conclusions hold",

which can be checked on random inputs. If one of these tests fails, either our reading of
the lemma is wrong, or the proof uses more than the Newton polygon at p. Both are worth
knowing, so look at the failing example before changing anything.

Run:  $SAGE_PYTHON -m pytest tests/ -v
 or:  $SAGE_PYTHON tests/test_properties.py     (no pytest needed)
"""

import os
import random
import sys
from fractions import Fraction
from math import comb

# Make "import laguerre" work when this file is run directly from any folder.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mpmath

from laguerre.arithmetic import (
    digit_sum,
    factorial_valuation,
    is_perfect_square,
    prime_divisors_of_delta,
    primes_up_to,
    section4_quantities,
    valuation,
)
from laguerre.newton_polygon import coefficient_valuation, dumas_degree_set, phi, polygon_summary
from laguerre.oracles import (
    evaluate_polynomial,
    laguerre_coefficients,
    proposition_1_3_candidates,
    signed_laguerre_coefficients,
    szego_root_bound,
)

NUMBER_OF_SAMPLES = 10000
SMALL_PRIMES = primes_up_to(50)


# ----------------------------------------------------------------------------------------
# Lemma 2.4 (Lucas) and Lemma 2.5 (Legendre).
# ----------------------------------------------------------------------------------------

def test_lemma_2_4_lucas():
    """C(m, m') = product of C(m_i, m'_i) (mod p) over the base-p digits; and its corollary."""
    rng = random.Random(1)
    for _ in range(NUMBER_OF_SAMPLES):
        p = rng.choice(SMALL_PRIMES)
        m = rng.randint(0, 5000)
        m_prime = rng.randint(0, m)

        product = 1
        remaining_m = m
        remaining_m_prime = m_prime
        while remaining_m > 0:
            # comb(u, v) is 0 when u < v, which is the convention of the lemma.
            product *= comb(remaining_m % p, remaining_m_prime % p)
            remaining_m //= p
            remaining_m_prime //= p
        assert comb(m, m_prime) % p == product % p

        # Consequence: if p | m and p does not divide m', then p | C(m, m').
        if m % p == 0 and m_prime % p != 0:
            assert comb(m, m_prime) % p == 0


def test_lemma_2_5_legendre():
    """nu_p(m!) = (m - sigma_p(m)) / (p - 1), compared with a direct count."""
    rng = random.Random(2)
    for _ in range(NUMBER_OF_SAMPLES):
        p = rng.choice(SMALL_PRIMES)
        m = rng.randint(0, 3000)
        direct_count = 0
        for term in range(1, m + 1):
            direct_count += valuation(term, p)
        assert (m - digit_sum(m, p)) % (p - 1) == 0
        assert factorial_valuation(m, p) == direct_count


# ----------------------------------------------------------------------------------------
# Lemma 2.9 and the valuation formula for the coefficients.
# ----------------------------------------------------------------------------------------

def test_lemma_2_9_divisibility_of_coefficients():
    """Lemma 2.9(i) and (ii), on the actual coefficients a_j."""
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(2, 60)
        a = rng.randint(1, 1000)
        coefficients = laguerre_coefficients(n, a)

        # (i)
        for j in range(0, n):
            assert coefficients[j] % n == 0
            assert coefficients[j] % (n + a) == 0
        for j in range(0, n - 1):
            assert coefficients[j] % (n - 1) == 0
            assert coefficients[j] % (n + a - 1) == 0

        # (ii)
        k = rng.randint(1, n // 2)
        primes = set(prime_divisors_of_delta(n - k + 1, k))
        primes.update(prime_divisors_of_delta(n + a - k + 1, k))
        for p in primes:
            assert coefficients[n] % p != 0
            for j in range(0, n - k + 1):
                assert coefficients[j] % p == 0


def test_coefficient_valuation_formula():
    """coefficient_valuation (Legendre) agrees with the valuation of the actual a_j."""
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(2, 60)
        a = rng.randint(1, 1000)
        p = rng.choice(SMALL_PRIMES)
        coefficients = laguerre_coefficients(n, a)
        for j in range(0, n + 1):
            assert coefficient_valuation(n, a, j, p) == valuation(coefficients[j], p)


# ----------------------------------------------------------------------------------------
# Lemmas 4.1, 4.2 and 4.3 (see the explanation at the top of this file).
# ----------------------------------------------------------------------------------------

def random_section4_sample(rng):
    """
    Draw random (n, a, k, p) with 50 < a <= 1000, 1 <= k <= 5, k <= n/2 and p a prime <= 50
    dividing Delta(n-k+1, k). Returns None if the draw has no such prime.
    """
    n = rng.randint(2, 500)
    a = rng.randint(51, 1000)
    k = rng.randint(1, min(5, n // 2))
    primes = [p for p in prime_divisors_of_delta(n - k + 1, k) if p <= 50]
    if len(primes) == 0:
        return None
    p = rng.choice(primes)
    return (n, a, k, p)


def test_lemmas_4_1_4_2_4_3():
    """The conclusions of Lemmas 4.1, 4.2 and 4.3, whenever k is in the Dumas set D_p."""
    rng = random.Random(5)
    number_tested = 0
    for _ in range(NUMBER_OF_SAMPLES):
        sample = random_section4_sample(rng)
        if sample is None:
            continue
        (n, a, k, p) = sample
        q = section4_quantities(n, a, k, p)
        (l, u0, j0, v0, t0, t1, c0) = (q["l"], q["u0"], q["j0"], q["v0"], q["t0"], q["t1"], q["c0"])

        # Hypothesis (8) of Lemma 4.1 with the largest allowed c, which is c = (p - 1) / k:
        #     p >= 1 + ck,   c >= 2,   (c - 1) / (p - 1) * (p^v0 + p) >= c0.
        c = Fraction(p - 1, k)
        if c < 2:
            continue
        if (c - 1) * (p**v0 + p) < c0 * (p - 1):
            continue
        # Replacement for "the polynomial has a factor of degree k".
        if k not in dumas_degree_set(n, a, p):
            continue
        number_tested += 1

        summary = polygon_summary(n, a, p)
        r1 = summary["r"][0]
        example = "(n, a, k, p) = (%d, %d, %d, %d)" % (n, a, k, p)

        # Lemma 4.1(i).
        assert j0 <= r1 < max(j0 + t1 * p**v0, p**v0 + p), example

        # Lemma 4.1(ii) and Lemma 4.2 need (p - 1) nu_p(t0 + 1) <= p^v0 (c - 1).
        if (p - 1) * valuation(t0 + 1, p) <= p**v0 * (c - 1):
            # Lemma 4.1(ii): r1 = j0, or r1 = p with l + 1 <= j0 < p <= j0 + k.
            assert r1 == j0 or (r1 == p and l + 1 <= j0 < p <= j0 + k), example
            # Lemma 4.2.
            assert j0 >= l + 1, example
            assert v0 >= u0 + 1, example
            if k == 1 and p == 3 and j0 == 2 and v0 - u0 == 2:
                assert r1 == p, example
            else:
                assert r1 == j0, example

        # Lemma 4.3.
        if p >= max(1 + 2 * k, 11):
            assert r1 == j0, example
            assert j0 >= l + 1, example
            assert v0 == 2 and u0 == 1, example
            assert j0 <= k <= j0 + l, example
            # The lemma also states "r2 != p". Its proof only excludes alternative (c) of
            # Lemma 4.1(ii), which is "r2 = p AND phi^(2) >= 1/k". The literal statement
            # r2 != p is false at the level of the Newton polygon: (n, a, k, p) =
            # (352, 845, 2, 11) has r1 = j0 = 2, r2 = 11 = p, and phi^(2) = 1/9 < 1/2.
            # So we test what the proof shows.
            if len(summary["r"]) >= 2:
                r2 = summary["r"][1]
                second_slope = summary["slopes"][1]
                assert not (r2 == p and second_slope >= Fraction(1, k)), example

    print("Lemmas 4.1-4.3: %d random inputs satisfied the hypotheses and were tested" % number_tested)
    assert number_tested > 0


def test_lemma_4_3_c0_is_2():
    """Used in the proof of Lemma 4.3: c0 = 2 for every prime p >= 11 and 50 < a <= 1000."""
    for p in SMALL_PRIMES:
        if p < 11:
            continue
        for a in range(51, 1001):
            # n = p and k = 1 make p divide Delta(n-k+1, k); c0 only depends on a and p.
            assert section4_quantities(p, a, 1, p)["c0"] == 2


def test_remark_1_slope_formulas():
    """
    Remark 1(ii) and (iii): when r1 = j0 and j0 < p,
        phi^(1) = v0 / j0            if j0 <= l,
        phi^(1) = (v0 - u0) / j0     if j0 >= l + 1.
    This mainly tests our definitions of l, u0, j0, v0 and of r1.
    """
    rng = random.Random(6)
    number_tested = 0
    for _ in range(NUMBER_OF_SAMPLES):
        sample = random_section4_sample(rng)
        if sample is None:
            continue
        (n, a, k, p) = sample
        if p <= k:
            continue
        q = section4_quantities(n, a, k, p)
        summary = polygon_summary(n, a, p)
        if summary["r"][0] != q["j0"] or q["j0"] == p:
            continue
        number_tested += 1
        if q["j0"] <= q["l"]:
            assert summary["slopes"][0] == Fraction(q["v0"], q["j0"])
        else:
            assert summary["slopes"][0] == Fraction(q["v0"] - q["u0"], q["j0"])
    assert number_tested > 0


# ----------------------------------------------------------------------------------------
# Lemma 6.2.
# ----------------------------------------------------------------------------------------

def test_lemma_6_2():
    """If p^m <= a < p^(m+1) and nu_p(n) >= m + 1, then phi_j(p) < 1/(p-1) for all 1 <= j <= n."""
    rng = random.Random(7)
    for _ in range(300):
        p = rng.choice(SMALL_PRIMES)
        a = rng.randint(51, 1000)
        m = 1
        while p**(m + 1) <= a:
            m += 1
        n = p**(m + 1) * rng.randint(1, 3)
        if n > 5000:
            continue
        for j in range(1, n + 1):
            assert phi(n, a, j, p) < Fraction(1, p - 1)


# ----------------------------------------------------------------------------------------
# Lemma 6.4 (Szego's bound), against numerically computed roots.
# ----------------------------------------------------------------------------------------

def test_lemma_6_4_root_bound():
    """All roots are real, positive, and at most B. (This is the only test that uses floats.)"""
    mpmath.mp.dps = 50
    rng = random.Random(8)
    for _ in range(50):
        n = rng.randint(2, 12)
        a = rng.randint(1, 1000)
        signed = signed_laguerre_coefficients(n, a)
        lowest_degree_first = [mpmath.mpf(coefficient) for coefficient in signed]
        roots = mpmath.polyroots(lowest_degree_first, maxsteps=500, extraprec=500, asc=True)
        assert len(roots) == n
        for root in roots:
            assert abs(mpmath.im(root)) < mpmath.mpf(10) ** (-20)
            assert mpmath.re(root) > 0
            # szego_root_bound returns the integer part of B, so B < szego_root_bound + 1.
            assert mpmath.re(root) < szego_root_bound(n, a) + 1


# ----------------------------------------------------------------------------------------
# Proposition 1.3, on the known integer roots of L_2^(a).
# ----------------------------------------------------------------------------------------

def test_proposition_1_3_on_known_roots():
    """
    For a + 2 = m^2 the roots of script-L_2^(a) are xi = a + 2 - m and xi = a + 2 + m.
    Both must be roots, be divisible as Proposition 1.3 says, and be among our candidates.
    """
    n = 2
    for a in range(4, 1001):
        if not is_perfect_square(a + 2):
            continue
        m = 0
        while m * m < a + 2:
            m += 1
        signed = signed_laguerre_coefficients(n, a)
        candidates = proposition_1_3_candidates(n, a)
        for xi in (a + 2 - m, a + 2 + m):
            assert evaluate_polynomial(signed, xi) == 0
            assert xi**n % n == 0
            assert xi**n % (n + a) == 0
            assert xi in candidates


# ----------------------------------------------------------------------------------------
# Running this file directly, without pytest.
# ----------------------------------------------------------------------------------------

if __name__ == "__main__":
    test_functions = [
        test_lemma_2_4_lucas,
        test_lemma_2_5_legendre,
        test_lemma_2_9_divisibility_of_coefficients,
        test_coefficient_valuation_formula,
        test_lemmas_4_1_4_2_4_3,
        test_lemma_4_3_c0_is_2,
        test_remark_1_slope_formulas,
        test_lemma_6_2,
        test_lemma_6_4_root_bound,
        test_proposition_1_3_on_known_roots,
    ]
    for test_function in test_functions:
        test_function()
        print("passed: %s" % test_function.__name__)
