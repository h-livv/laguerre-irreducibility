"""
STEP 4. Stormer data: all m with P(m(m-1)) <= 31 (Lehmer's Table IA), recomputed.

We enumerate all 31-smooth numbers up to STORMER_SEARCH_LIMIT (10^10) and collect the m for
which m - 1 is also 31-smooth.

Checkpoint: the largest such m is n_2 = 1,611,308,700 (the value the paper quotes from Lehmer).

IMPORTANT: this cross-checks Lehmer's table up to 10^10. That NO larger m exists is Lehmer's
theorem, which we import. The enumeration cannot prove it.

Optional: if you type Lehmer's Table IA into data/lehmer_table_IA_p31.txt (see the header of
that file), this script also compares the typed table with the recomputed one.

Run:  $SAGE_PYTHON step04_stormer_data.py
"""

import os

from laguerre.config import LEHMER_N2, LEHMER_TABLE_FILE, SMOOTH_BOUND, STORMER_SEARCH_LIMIT
from laguerre.reporting import StepReport
from laguerre.stormer import ends_of_smooth_blocks, read_lehmer_table, smooth_numbers_up_to


def main():
    report = StepReport("step04_stormer_data")

    smooth_set = smooth_numbers_up_to(STORMER_SEARCH_LIMIT, SMOOTH_BOUND)
    report.log("Number of %d-smooth numbers up to %d: %d"
               % (SMOOTH_BOUND, STORMER_SEARCH_LIMIT, len(smooth_set)))

    stormer_numbers = ends_of_smooth_blocks(smooth_set, 2)
    report.log("Number of m >= 2 with P(m(m-1)) <= %d: %d" % (SMOOTH_BOUND, len(stormer_numbers)))
    report.checkpoint("largest m <= 10^10 with P(m(m-1)) <= 31 (Lehmer's n_2)",
                      LEHMER_N2, stormer_numbers[-1])
    report.set_extra("stormer_numbers", stormer_numbers)

    typed_table = read_lehmer_table(LEHMER_TABLE_FILE)
    if len(typed_table) == 0:
        report.log("No typed copy of Lehmer's table found in data/%s; comparison skipped."
                   % os.path.basename(LEHMER_TABLE_FILE))
    else:
        only_in_typed_table = sorted(set(typed_table) - set(stormer_numbers))
        only_in_recomputation = sorted(set(stormer_numbers) - set(typed_table))
        report.checkpoint("entries of the typed Lehmer table missing from our recomputation",
                          [], only_in_typed_table)
        report.checkpoint("recomputed entries missing from the typed Lehmer table",
                          [], only_in_recomputation)

    report.save()


if __name__ == "__main__":
    main()
