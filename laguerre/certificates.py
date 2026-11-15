"""
Certificates: the final, explicit proof record for one case (n, a, k).

After the filters, a finite list of cases (n, a, k) remains. Each one must be closed by an
explicit computation. The record of that computation is a "certificate": a small dictionary
that is stored in the results/ folder. Its "type" entry is one of

    "newton_polygon"   a prime p for which Lemma 2.8 (Filaseta) excludes degree k
    "factorisation"    the degrees of the irreducible factors; none combine to k
    "root_search"      (k = 1 only) all possible integer roots were tested; none is a root
    "dumas"            a prime p whose Dumas degree set (Lemma 2.7) does not contain k
    "REDUCIBLE"        a factor of degree k EXISTS (expected only for the known exceptions)
    "OPEN"             no method above succeeded: the case is NOT closed
"""

from laguerre.arithmetic import prime_divisors_of_delta, primes_up_to, radical, subset_sums
from laguerre.config import FACTOR_LIMIT
from laguerre.newton_polygon import (
    dumas_degree_set,
    filaseta_excludes_degree,
    polygon_summary,
)
from laguerre.oracles import (
    direct_root_candidates,
    factor_degrees,
    find_integer_roots,
    proposition_1_3_candidates,
    szego_root_bound,
)


def newton_polygon_certificate(n, a, k):
    """
    Look for a prime p dividing Delta(n-k+1, k) * Delta(n+a-k+1, k) for which the right-most
    slope of NP_p is < 1/k (Lemma 2.8). Return the certificate, or None if no prime works.
    """
    primes = set(prime_divisors_of_delta(n - k + 1, k))
    primes.update(prime_divisors_of_delta(n + a - k + 1, k))
    for p in sorted(primes):
        if filaseta_excludes_degree(n, a, k, p):
            summary = polygon_summary(n, a, p)
            return {
                "type": "newton_polygon",
                "prime": p,
                "vertices": summary["vertices"],
                "rightmost_slope": str(summary["slopes"][0]),
            }
    return None


def factorisation_certificate(n, a, k):
    """
    Factorise the polynomial over Q. Return a "factorisation" certificate if no factor of
    degree k exists, and a "REDUCIBLE" record if one does.
    """
    degrees = factor_degrees(n, a)
    if k in subset_sums(degrees):
        return {"type": "REDUCIBLE", "factor_degrees": degrees}
    return {"type": "factorisation", "factor_degrees": degrees}


def root_search_certificate(n, a):
    """
    Decide whether there is a linear factor (k = 1) by testing every possible integer root.

    Two candidate lists are tested and both are recorded:
        * the direct list: all multiples of Rad(n(n+a)) in (0, B]   (complete on its own);
        * the shorter list that also uses Proposition 1.3            (the paper's method).
    The certificate is built from the direct list; the other one is a cross-check.
    """
    direct_candidates = direct_root_candidates(n, a)
    proposition_candidates = proposition_1_3_candidates(n, a)
    roots = find_integer_roots(n, a, direct_candidates)
    record = {
        "type": "root_search",
        "szego_bound": szego_root_bound(n, a),
        "radical_of_n_times_n_plus_a": radical(n * (n + a)),
        "number_of_direct_candidates": len(direct_candidates),
        "proposition_1_3_candidates": proposition_candidates,
        "roots_found": roots,
    }
    if len(roots) > 0:
        record["type"] = "REDUCIBLE"
    return record


def dumas_certificate(n, a, k):
    """
    Look for any prime p <= n + a whose Dumas degree set D_p(n, a) does not contain k
    (Lemma 2.7). Return the certificate, or None if no prime works.
    """
    for p in primes_up_to(n + a):
        if k not in dumas_degree_set(n, a, p):
            return {"type": "dumas", "prime": p}
    return None


def close_case(n, a, k):
    """
    Close the case (n, a, k) by the first method that works, in this order:

        1. Newton polygon (Lemma 2.8)                 cheap, and the paper's preferred method
        2. full factorisation, if n <= FACTOR_LIMIT
        3. integer-root search, if k = 1
        4. Dumas degree sets over all primes <= n + a

    Returns the certificate. Its type is "OPEN" if nothing worked.
    """
    certificate = newton_polygon_certificate(n, a, k)
    if certificate is not None:
        return certificate
    if n <= FACTOR_LIMIT:
        return factorisation_certificate(n, a, k)
    if k == 1:
        return root_search_certificate(n, a)
    certificate = dumas_certificate(n, a, k)
    if certificate is not None:
        return certificate
    return {"type": "OPEN"}
