"""
STEP 5. No factor of degree k >= 6 (Lemma 5.2). No computation on polynomials.

Lemma 5.2 is IMPORTED as an argument: its proof is a short deduction from Lemmas 2.1, 2.2,
2.3, 2.10 and 5.1. Here we only check, mechanically, the numerical statements that the
proof makes along the way. If one of them were false, the argument would not apply.

The setting (start of Section 5): by Lemma 2.10(ii) we may assume a > 5k, so with
a <= 1000 we get k <= 199.

Run:  $SAGE_PYTHON step05_k_at_least_6.py
"""

from laguerre.config import A_MAX, LEMMA_5_1_PRIME
from laguerre.reporting import StepReport

# Lemma 2.2 (Nair-Shorey) holds outside an exception set T. The values of k occurring in T:
LEMMA_2_2_EXCEPTION_K_VALUES = [2, 3, 4, 5, 7]


def main():
    report = StepReport("step05_k_at_least_6")

    # a > 5k and a <= A_MAX give k <= K_MAX.
    K_MAX = (A_MAX - 1) // 5
    report.checkpoint("largest k with 5k < a <= 1000 (the paper says k < 200)", 199, K_MAX)

    # "max(2k + 13, 541k/262) = 2k + 13, since k < 200", needed to apply Lemma 2.1.
    # 541k/262 <= 2k + 13 is the same as 541k <= 262 (2k + 13).
    holds = all(541 * k <= 262 * (2 * k + 13) for k in range(6, K_MAX + 1))
    report.checkpoint("for 6 <= k <= 199: max(2k+13, 541k/262) = 2k+13", True, holds)

    # Case k >= 18: "max(1 + 2k, 37) = 1 + 2k".
    holds = all(max(1 + 2 * k, LEMMA_5_1_PRIME) == 1 + 2 * k for k in range(18, K_MAX + 1))
    report.checkpoint("for k >= 18: max(1+2k, 37) = 1+2k", True, holds)

    # Case k >= 18: Lemma 2.2 is applied with m = n+a-k+1 > 6k+1 > 4k and gives a prime
    # p > 4.42k. The proof needs p > 37, that is 4.42k >= 37, written as 442k >= 3700.
    holds = all(442 * k >= 3700 for k in range(18, K_MAX + 1))
    report.checkpoint("for k >= 18: 4.42k >= 37", True, holds)

    # Case k >= 18: the exception set T of Lemma 2.2 only has k <= 7, so it does not interfere.
    holds = all(k < 18 for k in LEMMA_2_2_EXCEPTION_K_VALUES)
    report.checkpoint("the exception set T of Lemma 2.2 has no k >= 18", True, holds)

    # Both cases use Lemma 2.10(i) with a prime p > 37, which needs p^2 - p >= a.
    # p^2 - p increases with p, so it is enough to check p = 41, the first prime above 37.
    report.checkpoint("p^2 - p >= 1000 for the first prime p = 41 above 37", True, 41 * 41 - 41 >= A_MAX)

    # Case 6 <= k < 18: "max(1 + 2k, 37) = 37", and "n + a - k + 1 > 6k + 1 >= 37".
    holds = all(max(1 + 2 * k, LEMMA_5_1_PRIME) == LEMMA_5_1_PRIME for k in range(6, 18))
    report.checkpoint("for 6 <= k < 18: max(1+2k, 37) = 37", True, holds)
    holds = all(6 * k + 1 >= 37 for k in range(6, 18))
    report.checkpoint("for 6 <= k < 18: 6k+1 >= 37", True, holds)

    report.log("")
    report.log("Imported for this step: Lemma 2.1 (Laishram-Shorey), Lemma 2.2 (Nair-Shorey),")
    report.log("Lemma 2.3 (Najman), Lemma 2.10 (Laishram-Shorey), and the deduction of Lemma 5.2.")

    report.save()


if __name__ == "__main__":
    main()
