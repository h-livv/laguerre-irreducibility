"""
STEP 2. The cases n = 2 and n = 3 (Theorem 1.2), and an independent brute-force baseline.

Part A (n = 2). Theorem 1.2(i): L_2^(a) has a linear factor exactly when a + 2 is a perfect
        square. We factorise L_2^(a) for every a in the range and compare.

Part B (n = 3). Theorem 1.2(ii): if L_3^(a) has a linear factor then
            a even:  a + 3 = m^3,
            a odd:   a + 3 = 2 m^3  or  a + 3 = 4 m^3.
        We list the a of this shape (the paper finds 12), factorise them, and also check
        the theorem itself against the factorisation of L_3^(a) for every a in the range.

Part C (baseline). Factorise L_n^(a) for all 4 <= n <= BASELINE_MAX_N and all a in the
        range. This uses none of the paper's lemmas. It is an INDEPENDENT CHECK, not part
        of the proof (the proof must cover all n).

Part D (imported range). Spot-check the exceptions with a <= 50, which are imported from
        Laishram-Shorey: they must have a linear factor.

Run:  $SAGE_PYTHON step02_small_n_and_baseline.py     (Part C factorises about 26,000 polynomials)
"""

from laguerre.arithmetic import is_perfect_cube, is_perfect_square
from laguerre.certificates import factorisation_certificate
from laguerre.config import a_values
from laguerre.oracles import factor_degrees, is_irreducible
from laguerre.reporting import StepReport

BASELINE_MAX_N = 30

# The exceptions of Theorem 1.1 in the new range: n = 2, a = m^2 - 2 for 8 <= m <= 31.
PAPER_EXCEPTIONS_N2 = [m * m - 2 for m in range(8, 32)]

# The candidates for n = 3 listed in the proof of Lemma 6.6.
PAPER_CANDIDATES_N3 = [51, 105, 122, 125, 247, 253, 340, 429, 497, 683, 726, 861]

# The exceptions (n, a) with a <= 50 (imported from Laishram-Shorey, reference [10]).
IMPORTED_EXCEPTIONS = [(2, 2), (2, 7), (2, 14), (2, 23), (2, 34), (2, 47), (4, 5), (4, 23)]


def theorem_1_2_ii_allows(a):
    """Return True if a has the shape that Theorem 1.2(ii) requires for a linear factor."""
    if a % 2 == 0:
        return is_perfect_cube(a + 3)
    if (a + 3) % 2 == 0 and is_perfect_cube((a + 3) // 2):
        return True
    if (a + 3) % 4 == 0 and is_perfect_cube((a + 3) // 4):
        return True
    return False


def main():
    report = StepReport("step02_small_n_and_baseline")

    # ------------------------------------------------------------------ Part A: n = 2
    report.log("Part A: n = 2")
    reducible_n2 = [a for a in a_values() if not is_irreducible(2, a)]
    squares_n2 = [a for a in a_values() if is_perfect_square(a + 2)]
    report.checkpoint("n = 2: the a with L_2^(a) reducible (by factorisation)",
                      PAPER_EXCEPTIONS_N2, reducible_n2)
    report.checkpoint("n = 2: Theorem 1.2(i), reducible exactly when a + 2 is a square",
                      squares_n2, reducible_n2)
    report.set_extra("exceptions", [[2, a] for a in reducible_n2])

    # ------------------------------------------------------------------ Part B: n = 3
    report.log("")
    report.log("Part B: n = 3")
    candidates_n3 = [a for a in a_values() if theorem_1_2_ii_allows(a)]
    report.checkpoint("n = 3: the a allowed by Theorem 1.2(ii)", PAPER_CANDIDATES_N3, candidates_n3)
    reducible_n3 = [a for a in a_values() if not is_irreducible(3, a)]
    report.checkpoint("n = 3: the a with L_3^(a) reducible (by factorisation)", [], reducible_n3)
    theorem_holds = all(theorem_1_2_ii_allows(a) for a in reducible_n3)
    report.checkpoint("n = 3: every reducible L_3^(a) has the shape of Theorem 1.2(ii)",
                      True, theorem_holds)
    for a in candidates_n3:
        report.certificate(3, a, 1, factorisation_certificate(3, a, 1))

    # ------------------------------------------------------------------ Part C: baseline
    report.log("")
    report.log("Part C: baseline, 4 <= n <= %d (independent check, not part of the proof)" % BASELINE_MAX_N)
    reducible_baseline = []
    for n in range(4, BASELINE_MAX_N + 1):
        for a in a_values():
            if not is_irreducible(n, a):
                reducible_baseline.append((n, a))
        report.log("    n = %d done" % n)
    report.checkpoint("baseline: reducible (n, a) with 4 <= n <= %d" % BASELINE_MAX_N,
                      [], reducible_baseline)

    # ------------------------------------------------------------------ Part D: a <= 50
    report.log("")
    report.log("Part D: spot-check of the imported exceptions with a <= 50")
    with_linear_factor = [(n, a) for (n, a) in IMPORTED_EXCEPTIONS if 1 in factor_degrees(n, a)]
    report.checkpoint("imported exceptions (a <= 50) that have a linear factor",
                      IMPORTED_EXCEPTIONS, with_linear_factor)

    report.save()


if __name__ == "__main__":
    main()
