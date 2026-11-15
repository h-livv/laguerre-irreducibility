"""
STEP 8. No linear factor (k = 1) for n >= 4 (Lemmas 6.5 and 6.6).

(The cases n = 2 and n = 3 are Theorem 1.2 and are handled in step 2.)

By Lemma 6.3(ii), a linear factor forces n = 2^alpha * 3^beta * p^delta with explicit bounds
on the exponents. So only finitely many n are possible for each a. We list all pairs (n, a)
of this shape and apply the filters for k = 1 in this fixed order:

    Lemma 6.3, Lemma 6.2, Lemma 6.1          conditions on the primes dividing n
    Lemma 5.4(i), Lemma 5.4(ii)              conditions on the primes dividing n + a

Part A (Lemma 6.5): P(n) >= 5, that is, n has a prime factor p with 5 <= p <= 31.
        Paper: for 11 <= P(n) <= 31, 17 pairs remain before Lemma 5.4 and 3 after it.
        In total 19 pairs survive: the set S-tilde.

Part B (Lemma 6.6): P(n) <= 3, that is, n = 2^alpha * 3^beta, with n > 3.
        Paper: 366 pairs survive. Among them n = 512 occurs with 6 values of a, and 11 pairs
        have n > 300 and n != 512.

FOUND WHEN RUN:
  * Part A: our filters leave one pair more than the paper's S-tilde, (30, 699).
  * Part B: the paper's 366 is the count BEFORE the p = 3 condition of Lemma 5.4(ii) is used.
    With that condition we get 296 pairs. The paper's 6 values of a for n = 512 do use it;
    its 11 pairs with n > 300 do not (one of them, (768, 480), fails it).
  We reproduce the paper's numbers under its own reading and certify our own survivors.

Closing the survivors (both parts), as in the paper:
        n <= FACTOR_LIMIT (300):  full factorisation;
        n >  FACTOR_LIMIT:        integer-root search (Lemma 6.4 and Proposition 1.3).

Run:  $SAGE_PYTHON step08_k1_lemmas_6_5_6_6.py     (Part B factorises a few hundred polynomials
                                                    of degree up to 300; this is the slowest step)
"""

from laguerre.arithmetic import largest_prime_factor
from laguerre.certificates import factorisation_certificate, root_search_certificate
from laguerre.config import A_MAX, FACTOR_LIMIT, a_values
from laguerre.filters import lemma_5_4_i, lemma_5_4_ii, lemma_6_1, lemma_6_2, lemma_6_3
from laguerre.reporting import StepReport

# The exponent bounds of Lemma 6.3(ii).
MAX_ALPHA = A_MAX.bit_length() - 1          # floor(log2(1000)) = 9
MAX_BETA = 5
# (prime p, largest allowed exponent delta) for the primes 5 <= p <= 31.
LARGE_PRIMES_AND_MAX_EXPONENTS = [
    (5, 3), (7, 2), (11, 1), (13, 1), (17, 1), (19, 1), (23, 1), (29, 1), (31, 1),
]

PAPER_TILDE_S = [
    (5, 123), (5, 724), (10, 374), (20, 124), (22, 362), (25, 623), (25, 999), (40, 248),
    (40, 824), (40, 974), (56, 538), (152, 360), (160, 224), (200, 124), (320, 724),
    (400, 624), (640, 224), (896, 979), (6656, 844),
]
PAPER_A_VALUES_FOR_N_512 = [512, 576, 656, 664, 860, 948]
PAPER_LARGE_N_PAIRS = [
    (384, 480), (432, 80), (576, 160), (576, 482), (576, 674), (768, 294), (768, 753),
    (768, 480), (768, 584), (1152, 723), (1536, 512),
]


def lemma_5_4_i_for_k_1(n, a):
    """Lemma 5.4(i) with k = 1, in the two-argument form used by the filter list."""
    return lemma_5_4_i(n, a, 1)


# The filters for k = 1, in the order in which they are applied.
FILTERS = [
    ("Lemma 6.3", lemma_6_3),
    ("Lemma 6.2", lemma_6_2),
    ("Lemma 6.1", lemma_6_1),
    ("Lemma 5.4(i)", lemma_5_4_i_for_k_1),
    ("Lemma 5.4(ii)", lemma_5_4_ii),
]


def values_of_n_with_a_prime_at_least_5():
    """All n = 2^alpha * 3^beta * p^delta allowed by Lemma 6.3(ii) with delta >= 1."""
    values = []
    for (p, max_delta) in LARGE_PRIMES_AND_MAX_EXPONENTS:
        for delta in range(1, max_delta + 1):
            for alpha in range(0, MAX_ALPHA + 1):
                for beta in range(0, MAX_BETA + 1):
                    values.append(2**alpha * 3**beta * p**delta)
    return sorted(values)


def values_of_n_with_only_2_and_3():
    """All n = 2^alpha * 3^beta > 3 allowed by Lemma 6.3(ii)."""
    values = []
    for alpha in range(0, MAX_ALPHA + 1):
        for beta in range(0, MAX_BETA + 1):
            n = 2**alpha * 3**beta
            if n > 3:
                values.append(n)
    return sorted(values)


def apply_filters(report, label, pairs):
    """
    Apply the FILTERS one after the other to the list of pairs (n, a).
    Returns a dictionary: filter name -> the list of pairs that survive up to that filter.
    """
    report.log("%s: %d pairs (n, a) before the filters" % (label, len(pairs)))
    survivors_after = {}
    for (name, filter_function) in FILTERS:
        pairs = [(n, a) for (n, a) in pairs if filter_function(n, a)[0]]
        survivors_after[name] = pairs
        report.log("%s: %d pairs after %s" % (label, len(pairs), name))
    return survivors_after


def close_linear_case(report, n, a):
    """Close the case (n, a, k = 1): factorise if n is small, otherwise search integer roots."""
    if n <= FACTOR_LIMIT:
        report.certificate(n, a, 1, factorisation_certificate(n, a, 1))
    else:
        report.certificate(n, a, 1, root_search_certificate(n, a))


def main():
    report = StepReport("step08_k1_lemmas_6_5_6_6")

    # ------------------------------------------------------------------ Part A: Lemma 6.5
    pairs = [(n, a) for n in values_of_n_with_a_prime_at_least_5() for a in a_values()]
    survivors_after = apply_filters(report, "Part A (P(n) >= 5)", pairs)

    before_lemma_5_4 = [(n, a) for (n, a) in survivors_after["Lemma 6.1"] if largest_prime_factor(n) >= 11]
    report.checkpoint("Part A: pairs with 11 <= P(n) <= 31 before Lemma 5.4", 17, len(before_lemma_5_4))
    tilde_s = survivors_after["Lemma 5.4(ii)"]
    after_lemma_5_4 = [(n, a) for (n, a) in tilde_s if largest_prime_factor(n) >= 11]
    report.checkpoint("Part A: pairs with 11 <= P(n) <= 31 after Lemma 5.4",
                      [(22, 362), (152, 360), (6656, 844)], sorted(after_lemma_5_4))
    report.checkpoint("Part A: the set S-tilde", sorted(PAPER_TILDE_S), sorted(tilde_s),
                      explanation="We get one extra pair, (30, 699). It passes Lemmas 6.1, 6.2, 6.3 and 5.4 as "
                                  "we read them: 5^2 | (a+1), 3^3 | (a+3) with nu_3(n) = 1, and n + a = 3^6. "
                                  "No Newton polygon excludes it either (the right-most slope is >= 1 for "
                                  "p = 2, 3, 5). It is closed by factorisation: the polynomial is irreducible.")

    for (n, a) in tilde_s:
        close_linear_case(report, n, a)

    # ------------------------------------------------------------------ Part B: Lemma 6.6
    report.log("")
    pairs = [(n, a) for n in values_of_n_with_only_2_and_3() for a in a_values()]
    survivors_after = apply_filters(report, "Part B (n = 2^alpha 3^beta > 3)", pairs)
    survivors = survivors_after["Lemma 5.4(ii)"]

    # The paper's reading: its count 366 and its 11 large pairs are obtained WITHOUT the
    # p = 3 condition of Lemma 5.4(ii). We recompute that list only to compare the numbers.
    without_p_3 = [(n, a) for (n, a) in survivors_after["Lemma 5.4(i)"]
                   if lemma_5_4_ii(n, a, use_p_3=False)[0]]
    report.checkpoint("Part B: number of pairs, without the p = 3 condition of Lemma 5.4(ii)",
                      366, len(without_p_3))
    report.checkpoint("Part B: pairs with n > 300 and n != 512, without the p = 3 condition",
                      sorted(PAPER_LARGE_N_PAIRS),
                      sorted((n, a) for (n, a) in without_p_3 if n > 300 and n != 512))
    report.checkpoint("Part B: the values of a for n = 512, with the p = 3 condition",
                      PAPER_A_VALUES_FOR_N_512, sorted(a for (n, a) in survivors if n == 512))
    report.log("Part B: with the full Lemma 5.4(ii) we keep %d pairs. These get certificates." % len(survivors))
    report.log("Part B: pairs with n > 300 and n != 512 among them: %s"
               % (sorted((n, a) for (n, a) in survivors if n > 300 and n != 512),))

    for (n, a) in survivors:
        close_linear_case(report, n, a)

    # ------------------------------------------------- Details of root searches in the paper
    # These three values are printed in the proofs of Lemmas 6.5 and 6.6. They are computed
    # here even if the pair did not survive our filters, so that they can always be compared.
    report.log("")
    record = root_search_certificate(896, 979)
    report.checkpoint("(n, a) = (896, 979): candidates left by Proposition 1.3 (paper: xi = 2770, not a root)",
                      [2770], record["proposition_1_3_candidates"],
                      explanation="Our candidate list also requires Rad(n(n+a)) | xi (Remark 2 of the paper). "
                                  "Here Rad(896 * 1875) = 210 does not divide 2770, so 2770 is already excluded "
                                  "and no candidate is left. The conclusion (no integer root) is the same.")
    record = root_search_certificate(512, 512)
    report.checkpoint("(n, a) = (512, 512): candidates left by Proposition 1.3 (paper: xi = 2046, not a root)",
                      [2046], record["proposition_1_3_candidates"])
    record = root_search_certificate(400, 624)
    report.log("NOTE: the paper checks '128 possible values of xi' for (400, 624) but does not say")
    report.log("exactly how they are counted. We report the number of multiples of Rad(n(n+a)) in (0, B].")
    report.checkpoint("(n, a) = (400, 624): number of candidate xi checked (reading uncertain)",
                      128, record["number_of_direct_candidates"],
                      explanation="UNEXPLAINED. We count all multiples of Rad(n(n+a)) = 10 in (0, 2706]. Other "
                                  "readings we tried give 142 (xi sharing a factor with (n-1)(n+a-1)), 124, 112 "
                                  "and 94. All 270 candidates are tested and none is a root, so nothing is lost.")

    report.save()


if __name__ == "__main__":
    main()
