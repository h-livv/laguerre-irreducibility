"""
STEP 3. Lemma 2.6 by brute force.

Lemma 2.6. Let N <= 1005 be a positive integer. Then:

    (i)   There are no primes p, q with 7 <= p, q <= 31, p^2 | N and q^2 | (N - 1).
    (ii)  The only triples (N, p, q) with primes p, q >= 11, p^2 | N and q^2 | (N - 2)
          are (847, 11, 13) and (363, 11, 19).
    (iii) There is no prime p >= 7 with p^2 | (N - 2) and 5^3 | N (N - 1).

The bound 1005 is A_MAX + 5. We loop over every N and every prime and test divisibility.
We start at N = 3 so that N - 1 and N - 2 are positive.

Run:  $SAGE_PYTHON step03_lemma_2_6.py
"""

from laguerre.arithmetic import primes_up_to
from laguerre.config import A_MAX
from laguerre.reporting import StepReport

N_MAX = A_MAX + 5


def main():
    report = StepReport("step03_lemma_2_6")
    all_primes = primes_up_to(N_MAX)

    # (i)
    hits_i = []
    for N in range(3, N_MAX + 1):
        for p in all_primes:
            for q in all_primes:
                if 7 <= p <= 31 and 7 <= q <= 31:
                    if N % (p * p) == 0 and (N - 1) % (q * q) == 0:
                        hits_i.append((N, p, q))
    report.checkpoint("Lemma 2.6(i): triples (N, p, q)", [], hits_i)

    # (ii)
    hits_ii = []
    for N in range(3, N_MAX + 1):
        for p in all_primes:
            for q in all_primes:
                if p >= 11 and q >= 11:
                    if N % (p * p) == 0 and (N - 2) % (q * q) == 0:
                        hits_ii.append((N, p, q))
    report.checkpoint("Lemma 2.6(ii): triples (N, p, q)",
                      sorted([(847, 11, 13), (363, 11, 19)]), sorted(hits_ii))

    # (iii)
    hits_iii = []
    for N in range(3, N_MAX + 1):
        for p in all_primes:
            if p >= 7:
                if (N - 2) % (p * p) == 0 and (N * (N - 1)) % 125 == 0:
                    hits_iii.append((N, p))
    report.checkpoint("Lemma 2.6(iii): pairs (N, p)", [], hits_iii)

    report.save()


if __name__ == "__main__":
    main()
