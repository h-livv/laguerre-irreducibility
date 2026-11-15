"""
STEP 7. No factor of degree k = 2 (Lemma 5.6). Here n >= 4 and Delta(n-k+1, k) = n(n-1).

The stages, in the paper's order:

  Stage A  Lemma 5.1: P(n(n-1)) <= 31. By Lehmer's Table IA these n satisfy n <= n_2.
           We list them from the smooth-number enumeration.

  Stage B  Lemma 5.3: omega_7(n(n-1)) <= 1. The paper first uses Lehmer's Table IB to say
           that every n > 10^5 of stage A has omega_11(n(n-1)) >= 2 (so it is excluded),
           and then counts 59 values of n <= 10^5. We check both statements.

  Stage C  Lemma 5.3 with a: keep the pairs (n, a) that pass it. We split by P(n(n-1)):
             group "11 to 31": paper has 32 values of n and 118 pairs;
             group "7":        paper has 13 values of n, 21 values of a, 273 pairs;
             group "at most 5": n in {4, 5, 6, 9, 10, 16, 25, 81}, every a (no condition).

  Stage D  Lemma 5.4(i) and (iii) on every pair. Paper's survivors:
             group "11 to 31": none (via the sub-counts 106 / 12 / 8 / 0, which we also log);
             group "7":        (36, 339);
             group "at most 5": 4 pairs with n = 81, and 51 pairs with n != 81.

  Stage E  Every survivor gets a certificate (Newton polygon, or factorisation).

Run:  $SAGE_PYTHON step07_k2_lemma_5_6.py
"""

from laguerre.arithmetic import (
    largest_prime_factor_of_delta,
    omega_from_of_delta,
)
from laguerre.certificates import close_case
from laguerre.config import LEHMER_N2, SMOOTH_BOUND, a_values
from laguerre.filters import lemma_5_3, lemma_5_4_i, lemma_5_4_iii
from laguerre.reporting import StepReport
from laguerre.stormer import ends_of_smooth_blocks, smooth_numbers_up_to

K = 2


def survives_lemma_5_4(n, a):
    """Return True if the pair (n, a) passes both Lemma 5.4(i) and Lemma 5.4(iii) for k = 2."""
    (passes_i, reason_i) = lemma_5_4_i(n, a, K)
    (passes_iii, reason_iii) = lemma_5_4_iii(n, a)
    return passes_i and passes_iii


def main():
    report = StepReport("step07_k2_lemma_5_6")

    # ---------------------------------------------------------------------------- Stage A
    smooth_set = smooth_numbers_up_to(LEHMER_N2, SMOOTH_BOUND)
    stage_a = [n for n in ends_of_smooth_blocks(smooth_set, K) if n >= 4]
    report.log("Stage A: %d values of n >= 4 with P(n(n-1)) <= 31" % len(stage_a))
    report.checkpoint("Stage A: largest n with P(n(n-1)) <= 31 (Lehmer's n_2)", LEHMER_N2, stage_a[-1])

    # ---------------------------------------------------------------------------- Stage B
    large_n_all_excluded = all(omega_from_of_delta(n - 1, 2, 11) >= 2 for n in stage_a if n > 10**5)
    report.checkpoint("Stage B: every n > 10^5 has omega_11(n(n-1)) >= 2 (Lehmer's Table IB)",
                      True, large_n_all_excluded)

    stage_b = [n for n in stage_a if omega_from_of_delta(n - 1, 2, 7) <= 1]
    report.log("Stage B: n = %s" % (stage_b,))
    report.checkpoint("Stage B: number of n with P(n(n-1)) <= 31 and omega_7(n(n-1)) <= 1", 59, len(stage_b))
    report.checkpoint("Stage B: all these n are <= 10^5", True, all(n <= 10**5 for n in stage_b))

    # ---------------------------------------------------------------------------- Stage C
    pairs = {"11 to 31": [], "7": [], "at most 5": []}
    for n in stage_b:
        largest_prime = largest_prime_factor_of_delta(n - 1, 2)
        if largest_prime >= 11:
            group = "11 to 31"
        elif largest_prime == 7:
            group = "7"
        else:
            group = "at most 5"
        for a in a_values():
            (passes, reason) = lemma_5_3(n, a, K)
            if passes:
                pairs[group].append((n, a))

    def distinct_n(group):
        return sorted(set(n for (n, a) in pairs[group]))

    def distinct_a(group):
        return sorted(set(a for (n, a) in pairs[group]))

    report.checkpoint("Stage C, group 11 to 31: [number of n, number of pairs]",
                      [32, 118], [len(distinct_n("11 to 31")), len(pairs["11 to 31"])])
    report.checkpoint("Stage C, group 7: [number of n, number of a, number of pairs]",
                      [13, 21, 273], [len(distinct_n("7")), len(distinct_a("7")), len(pairs["7"])])
    report.checkpoint("Stage C, group at most 5: the values of n",
                      [4, 5, 6, 9, 10, 16, 25, 81], distinct_n("at most 5"))

    # ---------------------------------------------------------------------------- Stage D
    # Group "11 to 31": the paper's intermediate counts.
    group = pairs["11 to 31"]
    all_at_least_11 = all(largest_prime_factor_of_delta(n + a - 1, 2) >= 11 for (n, a) in group)
    report.checkpoint("Stage D, group 11 to 31: P((n+a)(n+a-1)) >= 11 for all pairs", True, all_at_least_11)
    at_least_37 = [(n, a) for (n, a) in group if largest_prime_factor_of_delta(n + a - 1, 2) >= 37]
    at_most_31 = [(n, a) for (n, a) in group if largest_prime_factor_of_delta(n + a - 1, 2) <= 31]
    report.checkpoint("Stage D, group 11 to 31: pairs with P((n+a)(n+a-1)) >= 37, and <= 31",
                      [106, 12], [len(at_least_37), len(at_most_31)])
    passing_bound = [(n, a) for (n, a) in at_least_37
                     if largest_prime_factor_of_delta(n + a - 1, 2) <= largest_prime_factor_of_delta(n - 3, 2)]
    report.checkpoint("Stage D, group 11 to 31: of these, P((n+a)(n+a-1)) <= P((n-3)(n-2))",
                      8, len(passing_bound))
    passing_5_4_i = [(n, a) for (n, a) in at_least_37 if lemma_5_4_i(n, a, K)[0]]
    report.checkpoint("Stage D, group 11 to 31: pairs with P >= 37 passing Lemma 5.4(i)", [], passing_5_4_i)
    passing_5_4_iii = [(n, a) for (n, a) in at_most_31 if lemma_5_4_iii(n, a)[0]]
    report.checkpoint("Stage D, group 11 to 31: pairs with P <= 31 passing Lemma 5.4(iii)", [], passing_5_4_iii)

    # All groups: the survivors of Lemma 5.4(i) and (iii).
    survivors = {}
    for group_name in pairs:
        survivors[group_name] = [(n, a) for (n, a) in pairs[group_name] if survives_lemma_5_4(n, a)]
        report.log("Stage D, group %s: survivors = %s" % (group_name, survivors[group_name]))

    report.checkpoint("Stage D, group 11 to 31: survivors", [], survivors["11 to 31"])
    report.checkpoint("Stage D, group 7: survivors", [(36, 339)], survivors["7"])
    survivors_81 = [(n, a) for (n, a) in survivors["at most 5"] if n == 81]
    survivors_small = [(n, a) for (n, a) in survivors["at most 5"] if n != 81]
    report.checkpoint("Stage D, group at most 5: survivors with n = 81",
                      [(81, 115), (81, 235), (81, 544), (81, 648)], survivors_81,
                      explanation="Lemma 5.4 as stated does not eliminate a = 144 and a = 360: "
                                  "225 * 224 has no prime >= 11, and for 441 * 440 the prime 11 satisfies "
                                  "11^2 | (a + 3). The paper does not say how it removes them. Both are "
                                  "closed below by a Newton polygon (p = 3, right-most slope 40/81 < 1/2).")
    report.checkpoint("Stage D, group at most 5: number of survivors with n != 81", 51, len(survivors_small))

    # ---------------------------------------------------------------------------- Stage E
    for group_name in pairs:
        for (n, a) in survivors[group_name]:
            report.certificate(n, a, K, close_case(n, a, K))

    report.save()


if __name__ == "__main__":
    main()
