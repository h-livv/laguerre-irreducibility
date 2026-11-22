"""
Constants shared by every script.

The paper proves its theorem for A_MIN < a <= A_MAX with A_MIN = 50 and A_MAX = 1000.
The range of a is read from here everywhere, so the scripts can be re-run with another A_MAX.
extension_a1078.py does that for 1000 < a <= 1078: it sets A_MIN and A_MAX at run time,
after checking that every use of a <= 1000 in the proofs still holds (see EXTENSION.md).

WARNING: the constants in the second block below are NOT free parameters. They are numbers
that the paper derives from a <= 1000. If you change A_MAX, the lemmas that use them are no
longer proved, and the run only tells you which checkpoints break.
"""

import os

# ----------------------------------------------------------------------------------------
# The range of the parameter a.
# ----------------------------------------------------------------------------------------

# The paper treats A_MIN < a <= A_MAX. The range a <= A_MIN is imported from Laishram-Shorey.
A_MIN = 50
A_MAX = 1000


def a_values():
    """Return every value of a in the new range: A_MIN < a <= A_MAX."""
    return range(A_MIN + 1, A_MAX + 1)


# ----------------------------------------------------------------------------------------
# Constants that the paper derives from a <= 1000 (do not change them independently).
# ----------------------------------------------------------------------------------------

# Lemma 5.1: a prime p >= max(1 + 2k, 37) dividing Delta(n-k+1, k) excludes a factor of
# degree k. The number 37 is the smallest prime with p^2 - p > 1000.
LEMMA_5_1_PRIME = 37

# Consequently every prime dividing Delta(n-k+1, k) is at most 31 (the prime before 37).
SMOOTH_BOUND = 31

# Lehmer (1964), Table IA: the largest m with P(m(m-1)) <= 31. Called n_2 in Lemma 5.6.
# This is an IMPORTED fact. Our enumeration (stormer.py) only cross-checks it.
LEHMER_N2 = 1611308700

# How far our own enumeration of 31-smooth numbers goes when cross-checking LEHMER_N2.
STORMER_SEARCH_LIMIT = 10**10

# ----------------------------------------------------------------------------------------
# Practical limits.
# ----------------------------------------------------------------------------------------

# Polynomials of degree n <= FACTOR_LIMIT are fully factorised over Q.
# Above this, we use Newton polygons and integer-root searches instead (as the paper does).
FACTOR_LIMIT = 300

# ----------------------------------------------------------------------------------------
# File locations.
# ----------------------------------------------------------------------------------------

REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIRECTORY = os.path.join(REPOSITORY_ROOT, "results")
DATA_DIRECTORY = os.path.join(REPOSITORY_ROOT, "data")
LEHMER_TABLE_FILE = os.path.join(DATA_DIRECTORY, "lehmer_table_IA_p31.txt")
