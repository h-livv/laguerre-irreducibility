"""
STEP 6. No factor of degree k = 3, 4, 5 (Lemma 5.5).

The proof of Lemma 5.5 is a sieve. We run its stages in the paper's order and compare each
count with the paper. A "pair" is (n, k); a "triple" is (n, a, k).

  Stage A  Lemma 5.1: every prime dividing Delta(n-k+1, k) is <= 31. By Lehmer's table these
           n are finitely many (n <= n_2). We list them from the smooth-number enumeration.
           Paper: 87 / 46 / 31 values of n for k = 3 / 4 / 5.

  Stage B  The exceptional set T-tilde: k = 5 and a in {358, 842}, where Lemma 5.3 allows TWO
           primes >= 11 in Delta(n-4, 5): 11 and 19 for a = 358, 11 and 13 for a = 842.
           Paper: 10 triples.

  Stage C  Lemma 5.3 (the part that only involves n and k): omega_11(Delta(n-k+1, k)) <= 1
           and nu_p(Delta(n-k+1, k)) <= 1 for 11 <= p <= 31.
           Paper: 31 / 14 / 6 values of n.

  Stage D  Split the pairs of stage C by P(Delta(n-k+1, k)):
             "large" pairs: P >= 11.  Paper: all n >= 11 except (n, k) = (16, 3).
             "small" pairs: P < 11.   Paper: n <= 10, and (16, 3).
           For the large pairs, Lemma 5.3 leaves only the a with p^2 || Delta(a+k-w+1, w).
           Paper: 186 / 96 / 87 pairs (n, a) for k = 3 / 4 / 5; with T-tilde 379 triples.

  Stage E  Lemma 5.4(i) on the 379 triples. Paper: 3 survivors,
           (25, 527, 3), (56, 845, 3), (65, 167, 3), each closed by a Newton polygon.

  Stage F  The small pairs: Lemma 5.4(i) for every a in the range.
           Paper: 228 / 36 / 2 pairs (n, a), 97 distinct (n, a), all closed by factorisation.

FOUND WHEN RUN: Stage D gives one more small pair than the paper, (n, k) = (50, 3), because
48 * 49 * 50 has no prime factor >= 11. The paper's counts do not include it. We keep it and
close its 38 cases in Stage F. The number 97 could not be reproduced (we get 228).

Every surviving triple gets a certificate, whether or not our counts equal the paper's.

Run:  $SAGE_PYTHON step06_k345_lemma_5_5.py
"""

from laguerre.arithmetic import (
    delta_valuation,
    largest_prime_factor_of_delta,
    prime_divisors_of_delta,
)
from laguerre.certificates import close_case, factorisation_certificate
from laguerre.config import LEHMER_N2, SMOOTH_BOUND, a_values
from laguerre.filters import lemma_5_3, lemma_5_4_i
from laguerre.reporting import StepReport
from laguerre.stormer import ends_of_smooth_blocks, smooth_numbers_up_to

K_VALUES = [3, 4, 5]

# Stage B: for these a (and k = 5), the two primes >= 11 that may both divide Delta(n-4, 5).
TILDE_T_PRIMES = {358: (11, 19), 842: (11, 13)}

PAPER_TILDE_T = [
    (13, 842, 5), (14, 842, 5), (15, 842, 5), (22, 358, 5), (23, 358, 5),
    (26, 842, 5), (58, 358, 5), (66, 842, 5), (156, 842, 5), (156, 358, 5),
]
PAPER_SMALL_PAIRS = [(6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (16, 3), (8, 4), (9, 4), (10, 4), (10, 5)]
PAPER_STAGE_E_SURVIVORS = [(25, 527, 3), (56, 845, 3), (65, 167, 3)]


def passes_stage_c(n, k):
    """Lemma 5.3, the part without a: at most one prime >= 11 divides Delta(n-k+1, k), once."""
    large_primes = [p for p in prime_divisors_of_delta(n - k + 1, k) if p >= 11]
    if len(large_primes) > 1:
        return False
    for p in large_primes:
        if delta_valuation(n - k + 1, k, p) != 1:
            return False
    return True


def main():
    report = StepReport("step06_k345_lemma_5_5")
    smooth_set = smooth_numbers_up_to(LEHMER_N2, SMOOTH_BOUND)

    # ---------------------------------------------------------------------------- Stage A
    stage_a = {}
    for k in K_VALUES:
        stage_a[k] = [n for n in ends_of_smooth_blocks(smooth_set, k) if n >= 2 * k]
        report.log("Stage A, k = %d: n = %s" % (k, stage_a[k]))
    report.checkpoint("Stage A: number of n with P(Delta(n-k+1,k)) <= 31, n >= 2k, for k = 3, 4, 5",
                      [87, 46, 31], [len(stage_a[k]) for k in K_VALUES])

    # ---------------------------------------------------------------------------- Stage B
    tilde_t = []
    for a in sorted(TILDE_T_PRIMES):
        (first_prime, second_prime) = TILDE_T_PRIMES[a]
        for n in stage_a[5]:
            primes = prime_divisors_of_delta(n - 4, 5)
            if first_prime in primes and second_prime in primes:
                tilde_t.append((n, a, 5))
    report.checkpoint("Stage B: the set T-tilde", sorted(PAPER_TILDE_T), sorted(tilde_t))

    # ---------------------------------------------------------------------------- Stage C
    stage_c = {}
    for k in K_VALUES:
        stage_c[k] = [n for n in stage_a[k] if passes_stage_c(n, k)]
        report.log("Stage C, k = %d: n = %s" % (k, stage_c[k]))
    report.checkpoint("Stage C: number of n after omega_11 <= 1 and nu_p <= 1, for k = 3, 4, 5",
                      [31, 14, 6], [len(stage_c[k]) for k in K_VALUES])

    # ---------------------------------------------------------------------------- Stage D
    large_pairs = []
    small_pairs = []
    for k in K_VALUES:
        for n in stage_c[k]:
            if largest_prime_factor_of_delta(n - k + 1, k) >= 11:
                large_pairs.append((n, k))
            else:
                small_pairs.append((n, k))
    report.checkpoint("Stage D: pairs (n, k) with P(Delta(n-k+1,k)) < 11",
                      sorted(PAPER_SMALL_PAIRS), sorted(small_pairs),
                      explanation="The paper says P(Delta(n-k+1,k)) >= 11 for all n >= 11 except (16, 3). "
                                  "But (n, k) = (50, 3) gives 48 * 49 * 50, whose largest prime is 7. The paper's "
                                  "count 186 for k = 3 matches ours only without n = 50, so this pair does not "
                                  "seem to be covered by the paper's counts. It is treated here in Stage F like "
                                  "the other small pairs (38 extra cases, all closed by factorisation).")

    stage_d = []
    for (n, k) in large_pairs:
        for a in a_values():
            (passes, reason) = lemma_5_3(n, a, k)
            if passes:
                stage_d.append((n, a, k))
    report.checkpoint("Stage D: number of pairs (n, a) after Lemma 5.3, for k = 3, 4, 5",
                      [186, 96, 87],
                      [len([triple for triple in stage_d if triple[2] == k]) for k in K_VALUES])

    triples = sorted(set(stage_d + tilde_t))
    report.checkpoint("Stage D: number of triples including T-tilde", 379, len(triples))

    # ---------------------------------------------------------------------------- Stage E
    below_37 = [(n, a, k) for (n, a, k) in triples
                if largest_prime_factor_of_delta(n + a - k + 1, k) < 37]
    report.checkpoint("Stage E: triples with P(Delta(n+a-k+1,k)) < 37",
                      sorted([(65, 167, 3), (25, 527, 3)]), sorted(below_37))

    stage_e = []
    for (n, a, k) in triples:
        (passes, reason) = lemma_5_4_i(n, a, k)
        if passes:
            stage_e.append((n, a, k))
    report.checkpoint("Stage E: survivors of Lemma 5.4(i)", sorted(PAPER_STAGE_E_SURVIVORS), sorted(stage_e))

    for (n, a, k) in stage_e:
        report.certificate(n, a, k, close_case(n, a, k))

    # ---------------------------------------------------------------------------- Stage F
    stage_f = []
    for (n, k) in small_pairs:
        for a in a_values():
            (passes, reason) = lemma_5_4_i(n, a, k)
            if passes:
                stage_f.append((n, a, k))
    # The paper's counts are for ITS list of small pairs, which does not contain (50, 3).
    stage_f_paper_pairs = [(n, a, k) for (n, a, k) in stage_f if (n, k) in PAPER_SMALL_PAIRS]
    report.checkpoint("Stage F: number of pairs (n, a) for the paper's small pairs, for k = 3, 4, 5",
                      [228, 36, 2],
                      [len([triple for triple in stage_f_paper_pairs if triple[2] == k]) for k in K_VALUES])
    distinct_pairs = sorted(set((n, a) for (n, a, k) in stage_f_paper_pairs))
    report.checkpoint(
        "Stage F: number of distinct (n, a) for the paper's small pairs", 97, len(distinct_pairs),
        explanation="UNEXPLAINED. The 228 pairs for k = 3 are already distinct, so the number of "
                    "distinct (n, a) cannot be below 228. We factorise all of them, so nothing is lost.")
    report.log("Stage F: our list has %d triples; %d of them come from the extra pair (50, 3)."
               % (len(stage_f), len(stage_f) - len(stage_f_paper_pairs)))

    for (n, a, k) in stage_f:
        report.certificate(n, a, k, factorisation_certificate(n, a, k))

    report.save()


if __name__ == "__main__":
    main()
