"""
Filters: the lemmas of the paper that eliminate cases.

Each function encodes the CONCLUSION of one lemma as a test on (n, a, k). The lemma says:
"if script-L_n^(a)(x) has a factor of degree k, then <condition>". So:

    the function returns (True,  reason)  if the condition holds:  the case SURVIVES,
    the function returns (False, reason)  if the condition fails:  NO factor of degree k.

The proofs of the lemmas are trusted here (they are in the paper). The `reason` string
says which part of the lemma decided, so that every elimination can be logged.

All lemmas below assume 50 < a <= 1000 and 1 <= k <= n/2. Several of them contain numbers
(31, 37, exponents) that the paper derives from a <= 1000; see laguerre/config.py.

EXACT READINGS. Where the printed statement of a lemma is ambiguous or differs from its
proof, the reading used here is written in the docstring under "Reading".
"""

from laguerre.arithmetic import (
    binomial_valuation,
    delta_valuation,
    largest_prime_factor,
    omega_from,
    omega_from_of_delta,
    prime_divisors,
    prime_divisors_of_delta,
    section4_quantities,
    valuation,
)
from laguerre.config import LEMMA_5_1_PRIME, SMOOTH_BOUND


# ----------------------------------------------------------------------------------------
# Lemma 2.10(i)  (Laishram-Shorey; imported statement).
# ----------------------------------------------------------------------------------------

def lemma_2_10_i(n, a, k):
    """
    Lemma 2.10(i). Let u0 = a / k. If there is a prime p >= k + 2 with

        p | Delta(n-k+1, k) * Delta(n+a-k+1, k),   p does not divide Delta(a+1, k),

    and ( p >= min(2 u0, k + u0)  or  ( p > 2k and p^2 - p >= a ) ),
    then there is no factor of degree k.

    The comparison p >= min(2a/k, k + a/k) is done as p*k >= min(2a, k*k + a), in integers.
    (This u0 = a/k is the notation of Lemma 2.10 only. It is not the u0 of Section 4.)
    """
    primes = set(prime_divisors_of_delta(n - k + 1, k))
    primes.update(prime_divisors_of_delta(n + a - k + 1, k))
    for p in sorted(primes):
        if p < k + 2:
            continue
        if delta_valuation(a + 1, k, p) > 0:
            continue
        first_condition = p * k >= min(2 * a, k * k + a)
        second_condition = p > 2 * k and p * p - p >= a
        if first_condition or second_condition:
            return (False, "Lemma 2.10(i): excluded by the prime p = %d" % p)
    return (True, "Lemma 2.10(i): no excluding prime")


# ----------------------------------------------------------------------------------------
# Lemma 4.3 and Lemma 5.1: primes dividing Delta(n-k+1, k).
# ----------------------------------------------------------------------------------------

def lemma_4_3(n, a, k):
    """
    Lemma 4.3. If there is a factor of degree k and p >= max(1 + 2k, 11) is a prime dividing
    Delta(n-k+1, k), then (in the notation of Section 4)

        j0 >= l + 1,   v0 = 2,   u0 = 1,   and   k is one of j0, j0 + 1, ..., j0 + l.

    (The lemma also says r1 = j0 and r2 != p, which are statements about the Newton polygon.
    They are not used here; tests/test_properties.py tests them. Note: "r2 != p" has to be
    read as "alternative (c) of Lemma 4.1(ii) does not occur"; see the comment in the test.)
    """
    for p in prime_divisors_of_delta(n - k + 1, k):
        if p < max(1 + 2 * k, 11):
            continue
        q = section4_quantities(n, a, k, p)
        if q["j0"] < q["l"] + 1:
            return (False, "Lemma 4.3: p = %d has j0 <= l" % p)
        if q["v0"] != 2 or q["u0"] != 1:
            return (False, "Lemma 4.3: p = %d does not have v0 = 2 and u0 = 1" % p)
        if not (q["j0"] <= k <= q["j0"] + q["l"]):
            return (False, "Lemma 4.3: p = %d has k outside j0, ..., j0 + l" % p)
    return (True, "Lemma 4.3: all conditions hold")


def lemma_5_1(n, a, k):
    """
    Lemma 5.1. If a prime p >= max(1 + 2k, 37) divides Delta(n-k+1, k), there is no factor
    of degree k.
    """
    for p in prime_divisors_of_delta(n - k + 1, k):
        if p >= max(1 + 2 * k, LEMMA_5_1_PRIME):
            return (False, "Lemma 5.1: excluded by the prime p = %d" % p)
    return (True, "Lemma 5.1: no excluding prime")


# ----------------------------------------------------------------------------------------
# Lemma 5.3: primes dividing Delta(n-k+1, k), for 1 <= k <= 5.
# ----------------------------------------------------------------------------------------

def lemma_5_3(n, a, k):
    """
    Lemma 5.3 (1 <= k <= 5). If there is a factor of degree k, then for every prime p
    dividing Delta(n-k+1, k):

        (1) p <= 31.
        (2) If 11 <= p <= 31:  nu_p(Delta(n-k+1, k)) = 1  and
                               p^2 || Delta(a + k - w + 1, w),  where w = ceil(k / 2).
            Written out, the second condition is:
                k = 1, 2:  p^2 || (a + k)
                k = 3, 4:  p^2 || (a + k - 1)(a + k)
                k = 5:     p^2 || (a + 3)(a + 4)(a + 5)
        (3) omega_11(Delta(n-k+1, k)) <= 1, except that <= 2 is allowed when k = 5 and
            a is 358 or 842.
        (4) Only for k = 2:  omega_7(n(n-1)) <= 1, and if 7 | n(n-1) then
            7^2 | (a + 2)  or  7^3 || (a + 4).

    Reading: in (2) the text extraction of the PDF shows "p || Delta(...)"; the PDF itself
    and the proof have "p^2 || Delta(...)". In (4) the paper adds "with p || n(n-1)" to the
    second alternative; like the paper's own count in Lemma 5.6 we do not use that extra
    condition (a weaker filter is still a correct filter).
    """
    primes = prime_divisors_of_delta(n - k + 1, k)

    for p in primes:
        if p > SMOOTH_BOUND:
            return (False, "Lemma 5.3 (1): the prime p = %d > 31 divides Delta(n-k+1, k)" % p)

    w = (k + 1) // 2
    for p in primes:
        if p < 11:
            continue
        if delta_valuation(n - k + 1, k, p) != 1:
            return (False, "Lemma 5.3 (2): p = %d divides Delta(n-k+1, k) more than once" % p)
        if delta_valuation(a + k - w + 1, w, p) != 2:
            return (False, "Lemma 5.3 (2): p^2 || Delta(a+k-w+1, w) fails for p = %d" % p)

    allowed_large_primes = 1
    if k == 5 and a in (358, 842):
        allowed_large_primes = 2
    if omega_from_of_delta(n - k + 1, k, 11) > allowed_large_primes:
        return (False, "Lemma 5.3 (3): too many primes >= 11 divide Delta(n-k+1, k)")

    if k == 2:
        if omega_from_of_delta(n - 1, 2, 7) > 1:
            return (False, "Lemma 5.3 (4): omega_7(n(n-1)) > 1")
        if 7 in primes:
            first_alternative = (a + 2) % 49 == 0
            second_alternative = valuation(a + 4, 7) == 3
            if not (first_alternative or second_alternative):
                return (False, "Lemma 5.3 (4): neither 7^2 | (a+2) nor 7^3 || (a+4)")

    return (True, "Lemma 5.3: all conditions hold")


# ----------------------------------------------------------------------------------------
# Lemma 5.4: primes dividing Delta(n+a-k+1, k), for 1 <= k <= 5.
# ----------------------------------------------------------------------------------------

def lemma_5_4_i(n, a, k):
    """
    Lemma 5.4(i) (1 <= k <= 5). If there is a factor of degree k, then every prime p >= 37
    dividing Delta(n+a-k+1, k) satisfies

        p || Delta(a+1, k)   and   p | Delta(n-2k+1, k).

    (The "moreover" of the lemma, P(Delta(n+a-k+1, k)) <= P(Delta(n-2k+1, k)), follows.)
    """
    for p in prime_divisors_of_delta(n + a - k + 1, k):
        if p < LEMMA_5_1_PRIME:
            continue
        if delta_valuation(a + 1, k, p) != 1:
            return (False, "Lemma 5.4(i): p || Delta(a+1, k) fails for p = %d" % p)
        if delta_valuation(n - 2 * k + 1, k, p) < 1:
            return (False, "Lemma 5.4(i): p = %d does not divide Delta(n-2k+1, k)" % p)
    return (True, "Lemma 5.4(i): all conditions hold")


def lemma_5_4_ii(n, a, use_p_3=True):
    """
    Lemma 5.4(ii) (k = 1). If there is a linear factor, then every prime p dividing n + a
    satisfies:

        p = 3:           r1 < 12
        p = 5:           5^j | (a + j) for some 1 <= j <= 4
        p = 7:           7^j | (a + j) for some 1 <= j <= 3
        11 <= p <= 31:   p | (a + 1)  or  p^2 | (a + 2)

    Reading of "r1 < 12" for p = 3: r1 is the length of the right-most edge, and by
    equation (15) it satisfies nu_3(Delta(a+1, r1)) - nu_3(C(n, r1)) >= r1. So the testable
    condition is: SOME j with 1 <= j <= 11 satisfies nu_3(Delta(a+1, j)) - nu_3(C(n, j)) >= j.

    With use_p_3=False the condition for p = 3 is skipped. This exists only to reproduce the
    count 366 of Lemma 6.6, which the paper evidently made before using the p = 3 condition.
    """
    for p in prime_divisors(n + a):
        if p == 3 and use_p_3:
            some_j_works = False
            for j in range(1, min(11, n) + 1):
                if delta_valuation(a + 1, j, 3) - binomial_valuation(n, j, 3) >= j:
                    some_j_works = True
                    break
            if not some_j_works:
                return (False, "Lemma 5.4(ii): p = 3, equation (15) fails for all r1 < 12")
        if p == 5:
            if not any(valuation(a + j, 5) >= j for j in range(1, 5)):
                return (False, "Lemma 5.4(ii): p = 5, no j <= 4 with 5^j | (a+j)")
        if p == 7:
            if not any(valuation(a + j, 7) >= j for j in range(1, 4)):
                return (False, "Lemma 5.4(ii): p = 7, no j <= 3 with 7^j | (a+j)")
        if 11 <= p <= SMOOTH_BOUND:
            if not ((a + 1) % p == 0 or (a + 2) % (p * p) == 0):
                return (False, "Lemma 5.4(ii): p = %d, neither p | (a+1) nor p^2 | (a+2)" % p)
    return (True, "Lemma 5.4(ii): all conditions hold")


def lemma_5_4_iii(n, a):
    """
    Lemma 5.4(iii) (k = 2). If there is a factor of degree 2, then every prime
    11 <= p <= 31 dividing (n + a)(n + a - 1) satisfies

        p | (a + 1)(a + 2)   or   p^2 | (a + 3)(a + 4).

    (The "moreover" of the lemma, p | Delta(n-5, 5), follows automatically from this
    condition together with p | (n + a)(n + a - 1), so it is not tested separately.)
    """
    for p in prime_divisors_of_delta(n + a - 1, 2):
        if p < 11 or p > SMOOTH_BOUND:
            continue
        first_alternative = delta_valuation(a + 1, 2, p) >= 1
        second_alternative = delta_valuation(a + 3, 2, p) >= 2
        if not (first_alternative or second_alternative):
            return (False, "Lemma 5.4(iii): both alternatives fail for p = %d" % p)
    return (True, "Lemma 5.4(iii): all conditions hold")


# ----------------------------------------------------------------------------------------
# Lemma 6.1: primes dividing n, for k = 1.
# ----------------------------------------------------------------------------------------

def _lemma_6_1_ii_holds(n, a, p):
    """
    Lemma 6.1(ii) for p = 5 or p = 7, p | n. There is a j >= 1 with p^(j+1) | (a + j) and

        nu_p(n) <= nu_p(a + 1) - 1    if j = 1,
        nu_p(n)  = nu_p(a + j) - j    if j >= 2.

    Reading: the lemma limits j by "j_7 = 3, j_5 = 4". For a <= 1000 the only possible
    cases are p^2 | (a+1), p^3 | (a+2) and 5^4 | (a+3) (these are the cases of the proof,
    and of the proof of Lemma 6.5). We simply try j = 1, 2, 3, 4; impossible ones never hold.
    """
    for j in range(1, 5):
        if (a + j) % p**(j + 1) != 0:
            continue
        if j == 1 and valuation(n, p) <= valuation(a + 1, p) - 1:
            return True
        if j >= 2 and valuation(n, p) == valuation(a + j, p) - j:
            return True
    return False


def _lemma_6_1_iii_holds(n, a):
    """
    Lemma 6.1(iii) for p = 3, 3 | n. Write u = nu_3(n). Exactly one of a+1, a+2, a+3 is
    divisible by 3, and one of the following holds:

      3 | (a+1):   3 || (a+1) and ( u <= nu_3(a+4) - 3  OR  u <= max(nu_3(a+4), nu_3(a+7)) - 5 )
                   3^2 | (a+1) and u <= nu_3(a+1) - 1
      3 | (a+2):   3 || (a+2) and u <= nu_3(a+5) - 4
                   3^3 | (a+2) and u <= nu_3(a+2) - 2
      3 | (a+3):   3 || (a+3) and u <= nu_3(a+6) - 4
                   3^3 | (a+3) and u = nu_3(a+3) - 2
                   3^6 | (a+3) and u = nu_3(a+3) - 5

    Reading (two places where the printed statement differs from its proof; in both we
    follow the PROOF, which gives the weaker and therefore safe condition):

      * 3 || (a+1): the statement joins the two inequalities with "and"; the proof
        derives "or".
      * 3^3 | (a+2): the statement has "u = nu_3(a+2) - 2"; the proof also allows
        v0 - u0 = 4 (Case I) and v0 - u0 >= 3 (Case II). Together: u <= nu_3(a+2) - 2.
    """
    u = valuation(n, 3)

    if (a + 1) % 3 == 0:
        if valuation(a + 1, 3) == 1:
            first = u <= valuation(a + 4, 3) - 3
            second = u <= max(valuation(a + 4, 3), valuation(a + 7, 3)) - 5
            return first or second
        return u <= valuation(a + 1, 3) - 1

    if (a + 2) % 3 == 0:
        if valuation(a + 2, 3) == 1:
            return u <= valuation(a + 5, 3) - 4
        return valuation(a + 2, 3) >= 3 and u <= valuation(a + 2, 3) - 2

    # Here 3 | (a + 3).
    if valuation(a + 3, 3) == 1:
        return u <= valuation(a + 6, 3) - 4
    if valuation(a + 3, 3) >= 3 and u == valuation(a + 3, 3) - 2:
        return True
    if valuation(a + 3, 3) >= 6 and u == valuation(a + 3, 3) - 5:
        return True
    return False


def lemma_6_1(n, a):
    """
    Lemma 6.1 (k = 1). If there is a linear factor, then every prime p dividing n satisfies
    p <= 31 and:

        (i)   11 <= p <= 31:  p^2 || (a + 1)  and  nu_p(n) = 1
        (ii)  p = 5 or 7:     see _lemma_6_1_ii_holds
        (iii) p = 3:          see _lemma_6_1_iii_holds

    The lemma says nothing for p = 2.
    """
    for p in prime_divisors(n):
        if p > SMOOTH_BOUND:
            return (False, "Lemma 6.1: the prime p = %d > 31 divides n" % p)
        if 11 <= p <= SMOOTH_BOUND:
            if valuation(a + 1, p) != 2 or valuation(n, p) != 1:
                return (False, "Lemma 6.1(i): fails for p = %d" % p)
        if p == 5 or p == 7:
            if not _lemma_6_1_ii_holds(n, a, p):
                return (False, "Lemma 6.1(ii): fails for p = %d" % p)
        if p == 3:
            if not _lemma_6_1_iii_holds(n, a):
                return (False, "Lemma 6.1(iii): fails for p = 3")
    return (True, "Lemma 6.1: all conditions hold")


# ----------------------------------------------------------------------------------------
# Lemma 6.2 and Lemma 6.3, for k = 1.
# ----------------------------------------------------------------------------------------

def lemma_6_2(n, a):
    """
    Lemma 6.2, used for k = 1. Let p be a prime and m >= 1 with p^m <= a < p^(m+1).
    If nu_p(n) >= m + 1, then every slope phi_j(p) is < 1/(p-1) <= 1. For a prime p | n,
    a linear factor needs phi^(1) >= 1 (equation (7)). So a linear factor forces

        nu_p(n) <= m   for every prime p | n with p <= a.
    """
    for p in prime_divisors(n):
        if p > a:
            continue
        m = 1
        while p**(m + 1) <= a:
            m += 1
        if valuation(n, p) >= m + 1:
            return (False, "Lemma 6.2: nu_p(n) is too large for p = %d" % p)
    return (True, "Lemma 6.2: all conditions hold")


def lemma_6_3(n, a):
    """
    Lemma 6.3 (k = 1). If there is a linear factor, then

        (i)   omega_5(n) <= 1  (at most one prime >= 5 divides n);
        (ii)  n = 2^alpha * 3^beta * p^delta with 5 <= p <= 31 and
              alpha <= floor(log2(a)),  beta <= 5,
              delta <= 3 if p = 5,  delta <= 2 if p = 7,  delta <= 1 if 11 <= p <= 31;
        (iii) P(n) < 11  or  P(n + a) < 11.
    """
    if omega_from(n, 5) > 1:
        return (False, "Lemma 6.3(i): omega_5(n) > 1")

    maximal_exponents = {3: 5, 5: 3, 7: 2}
    for p in prime_divisors(n):
        if p > SMOOTH_BOUND:
            return (False, "Lemma 6.3(ii): the prime p = %d > 31 divides n" % p)
        if p == 2:
            if 2 ** valuation(n, 2) > a:
                return (False, "Lemma 6.3(ii): nu_2(n) > floor(log2(a))")
        else:
            if valuation(n, p) > maximal_exponents.get(p, 1):
                return (False, "Lemma 6.3(ii): nu_p(n) is too large for p = %d" % p)

    if largest_prime_factor(n) >= 11 and largest_prime_factor(n + a) >= 11:
        return (False, "Lemma 6.3(iii): P(n) >= 11 and P(n+a) >= 11")

    return (True, "Lemma 6.3: all conditions hold")
