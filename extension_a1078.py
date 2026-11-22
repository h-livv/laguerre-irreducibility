"""
EXTENSION. Theorem 1.1 for 1000 < a <= 1078, with the paper's own arguments.

The paper proves irreducibility of L_n^(a)(x) for a <= 1000. Its concluding remarks say the
bound "is not intended to be sharp". This script asks how far the proof goes UNCHANGED:

  Part 1  Audit. Every place where the proof uses "a <= 1000" is written below as an
          inequality in a bound A on a. For each one we compute the largest A for which it
          still holds (scanning A upwards). The smallest of these is the new bound A_EXT.
          The finite statements that were checked by computer for a <= 1000 (Lemma 2.6, and
          the special values of a named in the proofs of Lemmas 5.3 and 6.3) are recomputed.

  Part 2  Sieve. The steps of the reproduction (2, 6, 7, 8) are re-run on the NEW range only,
          1000 < a <= A_EXT, with exactly the same filter and certificate code. Their output
          goes to results/extension_a1078/, so the a <= 1000 results are not touched.
          The paper's checkpoint values refer to a <= 1000 and do not apply here, so the
          checkpoints of those steps are logged as plain counts (no paper column).

  Part 3  Summary. results/extension_a1078/summary.md: verdict, audit table, certificates.

What is assumed is exactly what the a <= 1000 reproduction assumes (DOCUMENTATION.md,
"What is imported, not verified"): the imported results of the literature, and the PROOFS of
the filter lemmas, whose numerical hypotheses are the ones audited in Part 1.

Run:  $SAGE_PYTHON extension_a1078.py
"""

import json
import math
import os
import sys

# --------------------------------------------------------------------------------------------
# The range. Set BEFORE any other import from laguerre or from the step scripts, because they
# read A_MIN, A_MAX and RESULTS_DIRECTORY when they are imported.
# --------------------------------------------------------------------------------------------

import laguerre.config as config

A_OLD = 1000                    # the paper's bound
A_EXT = 1078                    # the bound reached by Part 1 (checked again at run time)
OUTPUT_DIRECTORY = os.path.join(config.REPOSITORY_ROOT, "results", "extension_a1078")

config.A_MIN = A_OLD
config.A_MAX = A_EXT
config.RESULTS_DIRECTORY = OUTPUT_DIRECTORY

from laguerre.arithmetic import primes_up_to  # noqa: E402
import laguerre.reporting as reporting                  # noqa: E402

# Upper end of the scan in Part 1. Every audited inequality fails somewhere below this.
SCAN_LIMIT = 5000


# ============================================================================================
# Part 1. The audit.
# ============================================================================================

def c0(a, p):
    """The least positive integer c0 with a + p + p^2 <= (p - 1) p^c0  (equation (6))."""
    c = 1
    while a + p + p * p > (p - 1) * p**c:
        c += 1
    return c


def lemma_2_6_hits(n_max):
    """All solutions of the three statements of Lemma 2.6 with N <= n_max."""
    small = [p for p in primes_up_to(31) if p >= 7]
    large = [p for p in primes_up_to(math.isqrt(n_max) + 1) if p >= 11]
    hits_i = [(N, p, q) for N in range(3, n_max + 1) for p in small for q in small
              if N % (p * p) == 0 and (N - 1) % (q * q) == 0]
    hits_ii = [(N, p, q) for N in range(3, n_max + 1) for p in large for q in large
               if N % (p * p) == 0 and (N - 2) % (q * q) == 0]
    hits_iii = [(N, p) for N in range(3, n_max + 1)
                for p in primes_up_to(math.isqrt(n_max) + 1) if p >= 7
                if (N - 2) % (p * p) == 0 and (N * (N - 1)) % 125 == 0]
    return hits_i, hits_ii, hits_iii


# The exceptions of Lemma 2.6 that the paper handles (and whose a lie below 1000).
LEMMA_2_6_KNOWN = ([], [(363, 11, 19), (847, 11, 13)], [])


def lemma_5_2_window_ok(A):
    """
    Lemma 5.2, case k >= 18, for every k with 5k < a <= A.

    Lemma 2.1 gives P(Delta(n-k+1, k)) > 2k once n >= M(k) = max(2k+13, ceil(541k/262)); with
    Lemma 5.1 this forces n <= M(k) - 1. The proof then needs a prime p > 4.42k (Lemma 2.2)
    with p <= n - 1, a contradiction when M(k) - 2 < 4.42k. The paper writes M(k) = 2k+13,
    which is true for k <= 200 only; for larger k we use M(k) itself.
    """
    k_max = (A - 1) // 5
    for k in range(18, k_max + 1):
        m_k = max(2 * k + 13, -(-541 * k // 262))
        if 100 * (m_k - 2) >= 442 * k:
            return False
    return True


def special_a_for_lemma_6_3(A):
    """
    Proof of Lemma 6.3(i): if 5*7 | n and 7^3 | (a+2), it needs one of the p = 5 conditions
    of Lemma 6.1(ii) to fail, i.e. none of 5^2 | (a+1), 5^3 | (a+2), 5^4 | (a+3).
    (The paper lists a in {341, 684}; for larger A there are more such a.)
    """
    for a in range(51, A + 1):
        if (a + 2) % 343 == 0:
            if (a + 1) % 25 == 0 or (a + 2) % 125 == 0 or (a + 3) % 625 == 0:
                return False
    return True


def special_a_for_lemma_5_3(A):
    """
    Proof of Lemma 5.3, k = 2, p = 7: for the a with 7^3 | (a+4) (the paper's {339, 682}),
    it needs that no prime q > 7 has q^2 | (a+2).
    """
    for a in range(51, A + 1):
        if (a + 4) % 343 == 0:
            m = a + 2
            if any(m % (q * q) == 0 for q in primes_up_to(math.isqrt(m) + 1) if q > 7):
                return False
    return True


# Each entry: (where in the paper, the statement as a test on the bound A).
# A test must say whether the statement holds for ALL a with 50 < a <= A.
AUDIT = [
    ("Lemma 4.2: p^v0 <= a + p < p^5 for p >= 5, so v0 <= 4",
     lambda A: all(A + p < p**5 for p in [5, 7, 11, 13])),
    ("Lemma 4.3: c0 = 2 for every prime p >= 11 (eq. (6): a + p + p^2 <= (p-1)p^2)",
     lambda A: all(c0(A, p) == 2 for p in primes_up_to(200) if p >= 11)),
    ("Lemma 5.1: a + p < p^2 for p >= 37",
     lambda A: A + 37 < 37 * 37),
    ("Lemma 5.2: p^2 - p >= a for the primes p >= 41 used with Lemma 2.10(i)",
     lambda A: 41 * 41 - 41 >= A),
    ("Lemma 5.2: the window n <= M(k) - 1 contradicts p > 4.42k for all 18 <= k < a/5",
     lemma_5_2_window_ok),
    ("Lemma 5.3, k = 2, p = 7: c0 = 3 (taken in the proof)",
     lambda A: c0(A, 7) <= 3),
    ("Lemma 5.3, k = 2, p = 7: 7^4 > a + 4, so 7^3 || (a+2)(a+4)",
     lambda A: 7**4 > A + 4),
    ("Lemma 5.3, k = 2, p = 7: p^2 q^2 > a + 2 for primes 7 <= p < q",
     lambda A: 7 * 7 * 11 * 11 > A + 2),
    ("Lemma 5.3, k = 2, p = 7: no q > 7 with q^2 | (a+2) when 7^3 | (a+4)",
     special_a_for_lemma_5_3),
    ("Lemma 5.4, table: v~ <= 1 for p >= 37 (p^2 > a + r1, r1 < p)",
     lambda A: 37 * 37 > A + 36),
    ("Lemma 5.4, table: v~ <= 2 for p >= 11 (p^3 > a + 3(p-1))",
     lambda A: 11**3 > A + 3 * 10),
    ("Lemma 5.4, table: v~ <= 3 for p = 7 (7^4 > a + 4*6)",
     lambda A: 7**4 > A + 24),
    ("Lemma 5.4, table: v~ <= 4 for p = 5 (5^5 > a + 5*4)",
     lambda A: 5**5 > A + 20),
    ("Lemma 5.4, table: v~ <= 6 for p = 3 (3^7 > a + 7*2)",
     lambda A: 3**7 > A + 14),
    ("Lemma 5.4(i): nu_p(Delta(a+1, p)) = 1 for p >= 37",
     lambda A: 37 * 37 > A + 37),
    ("Lemma 5.4(iii): no p >= 11 with p^3 | a + j, j <= 5",
     lambda A: 11**3 > A + 5),
    ("Lemma 6.1(ii): c0 <= p - 1 for p = 5 and p = 7",
     lambda A: c0(A, 5) <= 4 and c0(A, 7) <= 6),
    ("Lemma 6.1(iii): c0 <= 6 and v0 <= 6 for p = 3",
     lambda A: c0(A, 3) <= 6 and 3**7 > A + 3),
    ("Lemma 6.1(iii), v0 = 1: 3^v - a < 2v forces v <= 6",
     lambda A: all(3**v - A >= 2 * v for v in range(7, 20))),
    ("Lemma 6.3(i): 7^2 * 5^2 > a + 1 and 5^2 * 11^2 > a + 1",
     lambda A: 49 * 25 > A + 1),
    ("Lemma 6.3(i): 7^3 | (a+2) is incompatible with Lemma 6.1(ii) for p = 5",
     special_a_for_lemma_6_3),
    ("Lemma 6.3(iii): p^2 q > a + 1 for p, q >= 11",
     lambda A: 11**3 > A + 1),
    ("Lemma 2.6, N <= a + 5: no solutions beyond the paper's two",
     lambda A: lemma_2_6_hits(A + 5) == LEMMA_2_6_KNOWN),
]


def largest_valid_bound(test):
    """The largest A <= SCAN_LIMIT such that test(A') holds for every A' <= A (A' >= 1000)."""
    if not test(A_OLD):
        return None
    A = A_OLD
    while A < SCAN_LIMIT and test(A + 1):
        A += 1
    return A


def run_audit():
    rows = []
    for (description, test) in AUDIT:
        bound = largest_valid_bound(test)
        rows.append({"statement": description, "largest_A": bound, "holds_at_A_EXT": bool(test(A_EXT))})
        print("  %-90s %s" % (description, bound))
    return rows


# ============================================================================================
# Part 2. The sieve on the new range, re-using the steps of the reproduction.
# ============================================================================================

def checkpoint_as_count(self, description, paper_value, our_value, explanation=""):
    """Replacement for StepReport.checkpoint: the paper's values are for a <= 1000."""
    self.log("COUNT  %s: %s" % (description, our_value))
    self.checkpoints.append({"description": description, "ours": our_value, "matches": True})


SIEVE_STEPS = [
    "step02_small_n_and_baseline",
    "step06_k345_lemma_5_5",
    "step07_k2_lemma_5_6",
    "step08_k1_lemmas_6_5_6_6",
]


def run_sieve():
    reporting.StepReport.checkpoint = checkpoint_as_count
    sys.path.insert(0, config.REPOSITORY_ROOT)
    for step_name in SIEVE_STEPS:
        print("\n=== %s on %d < a <= %d" % (step_name, config.A_MIN, config.A_MAX))
        module = __import__(step_name)
        module.main()


# ============================================================================================
# Part 3. Summary.
# ============================================================================================

def write_summary(audit_rows):
    bound = min(row["largest_A"] for row in audit_rows)
    binding = [row["statement"] for row in audit_rows if row["largest_A"] == bound]

    certificates = []
    for step_name in SIEVE_STEPS:
        with open(os.path.join(OUTPUT_DIRECTORY, step_name + ".json")) as json_file:
            data = json.load(json_file)
        for certificate in data["certificates"]:
            certificates.append((step_name, certificate))
        if step_name == "step02_small_n_and_baseline":
            exceptions = data["extra"].get("exceptions", [])
            baseline = [c["ours"] for c in data["checkpoints"] if c["description"].startswith("baseline")]

    expected_exceptions = [[2, a] for a in range(A_OLD + 1, A_EXT + 1) if math.isqrt(a + 2)**2 == a + 2]
    open_cases = [c for (s, c) in certificates if c["certificate"]["type"] == "OPEN"]
    reducible = [c for (s, c) in certificates if c["certificate"]["type"] == "REDUCIBLE"]
    counts = {}
    for (step_name, c) in certificates:
        key = (step_name, c["certificate"]["type"])
        counts[key] = counts.get(key, 0) + 1

    verdict = (bound >= A_EXT and not open_cases and not reducible
               and exceptions == expected_exceptions and baseline == [[]])

    lines = ["# Extension: Laguerre irreducibility for %d < a <= %d" % (A_OLD, A_EXT), ""]
    lines.append("## 1. Outcome")
    lines.append("")
    if verdict:
        lines.append("For %d < a <= %d and n >= 2, the computations of the paper's proof go through "
                     "unchanged: the only reducible L_n^(a) are n = 2, a + 2 a perfect square, "
                     "that is a = %s." % (A_OLD, A_EXT, [e[1] for e in exceptions]))
    else:
        lines.append("The extension does NOT go through; see below.")
    lines.append("")
    lines.append("- largest A allowed by the audit: %d (binding: %s)" % (bound, "; ".join(binding)))
    lines.append("- exceptions found (n, a): %s (expected %s)" % (exceptions, expected_exceptions))
    lines.append("- cases left OPEN: %s" % ([(c["n"], c["a"], c["k"]) for c in open_cases],))
    lines.append("- REDUCIBLE cases among the certificates: %s" % ([(c["n"], c["a"], c["k"]) for c in reducible],))
    lines.append("- brute-force baseline 4 <= n <= 30, reducible pairs: %s" % (baseline,))
    lines.append("")
    lines.append("## 2. Audit: where the proof uses a <= 1000")
    lines.append("")
    lines.append("| Statement | Holds for all a <= A, largest A | Holds at A = %d |" % A_EXT)
    lines.append("| --- | --- | --- |")
    for row in sorted(audit_rows, key=lambda r: r["largest_A"]):
        shown = row["largest_A"] if row["largest_A"] < SCAN_LIMIT else ">= %d" % SCAN_LIMIT
        lines.append("| %s | %s | %s |" % (row["statement"], shown, "yes" if row["holds_at_A_EXT"] else "NO"))
    lines.append("")
    lines.append("## 3. Certificates")
    lines.append("")
    lines.append("| Step | Certificate type | Number of cases |")
    lines.append("| --- | --- | --- |")
    for (step_name, kind) in sorted(counts):
        lines.append("| %s | %s | %d |" % (step_name, kind, counts[(step_name, kind)]))
    lines.append("")
    lines.append("The per-step logs and certificates are in this folder. The counts logged as COUNT")
    lines.append("are for the new range only; the paper's values (for a <= 1000) do not apply to them.")
    lines.append("")
    lines.append("## 4. Assumed, not verified")
    lines.append("")
    lines.append("The same imports as the a <= 1000 reproduction (see ../summary.md, section 4), and the")
    lines.append("proofs of the filter lemmas, read with a <= %d in place of a <= 1000. Section 2 lists" % A_EXT)
    lines.append("every place where those proofs use the bound on a.")

    with open(os.path.join(OUTPUT_DIRECTORY, "summary.md"), "w") as summary_file:
        summary_file.write("\n".join(lines) + "\n")
    with open(os.path.join(OUTPUT_DIRECTORY, "audit.json"), "w") as audit_file:
        json.dump({"A_EXT": A_EXT, "largest_A": bound, "binding": binding, "rows": audit_rows,
                   "verdict": verdict, "exceptions": exceptions}, audit_file, indent=1)
    print("\nVerdict: %s. Wrote %s" % (verdict, os.path.join(OUTPUT_DIRECTORY, "summary.md")))
    return verdict


def main():
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    print("Part 1: audit of the bound a <= 1000 (largest A for which each statement holds)")
    audit_rows = run_audit()
    bound = min(row["largest_A"] for row in audit_rows)
    if bound < A_EXT:
        print("The audit allows only A = %d < A_EXT = %d. Stopping." % (bound, A_EXT))
        sys.exit(1)
    run_sieve()
    write_summary(audit_rows)


if __name__ == "__main__":
    main()
