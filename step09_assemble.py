"""
STEP 9. Assemble the results of steps 1 to 8 into one summary.

This script computes nothing new. It reads the results/*.json files written by the other
steps and writes results/summary.md with:

    1. the outcome: do the computations agree with Theorem 1.1 on 50 < a <= 1000?
    2. the checkpoint table: every number printed in the paper next to ours;
    3. the certificates: how many of each type, and any case that is NOT closed;
    4. the list of imported results (assumptions that are not verified here).

The computations count as agreeing with the theorem when all steps have run, no certificate
is OPEN or REDUCIBLE, and the exception list found in step 2 is exactly n = 2, a = m^2 - 2
for 8 <= m <= 31. This is a re-run of the finite computations of the paper's proof. It is
NOT an independent proof: the lemmas listed under "imports" are taken as given. Checkpoint differences are listed but do not change
the verdict: a different intermediate count is a question about the paper's wording, as
long as every case that survived OUR filters is closed by a certificate.

Run:  $SAGE_PYTHON step09_assemble.py      (plain python3 also works for this step)
"""

import json
import os

from laguerre.config import A_MAX, A_MIN, RESULTS_DIRECTORY

STEP_NAMES = [
    "step01_newton_polygon_tables",
    "step02_small_n_and_baseline",
    "step03_lemma_2_6",
    "step04_stormer_data",
    "step05_k_at_least_6",
    "step06_k345_lemma_5_5",
    "step07_k2_lemma_5_6",
    "step08_k1_lemmas_6_5_6_6",
]

EXPECTED_EXCEPTIONS = [[2, m * m - 2] for m in range(8, 32)]

IMPORTS = [
    "Lemma 2.1 (Laishram-Shorey 2005): P(Delta(m-k+1, k)) > 2k.",
    "Lemma 2.2 (Nair-Shorey 2015): P(Delta(m, k)) > 4.42k outside the exception set T.",
    "Lemma 2.3 (Najman 2011): P(Delta(m, 6)) > 31 for m > 31, and > 37 for m > 37.",
    "Lemma 2.10 (Laishram-Shorey 2011): the prime criterion (i) and the range a <= 5k (ii).",
    "Lemma 5.2: the deduction that there is no factor of degree k >= 6 (hypotheses checked in step 5).",
    "Lehmer 1964, Tables IA and IB: no m > 1,611,308,700 has P(m(m-1)) <= 31.",
    "Szego, Theorems 6.31.2-3: the bounds on the zeros of Laguerre polynomials (Lemma 6.4).",
    "Laishram-Shorey 2011, Theorem 1: the whole range 0 <= a <= 50.",
    "The proofs of the filter lemmas 4.1-4.3, 5.1, 5.3, 5.4, 6.1-6.3 and of Proposition 1.3.",
]


def main():
    lines = []
    lines.append("# Summary: Laguerre irreducibility for %d < a <= %d" % (A_MIN, A_MAX))
    lines.append("")

    # Load the result file of each step.
    results = {}
    missing_steps = []
    for step_name in STEP_NAMES:
        path = os.path.join(RESULTS_DIRECTORY, step_name + ".json")
        if os.path.exists(path):
            with open(path) as json_file:
                results[step_name] = json.load(json_file)
        else:
            missing_steps.append(step_name)

    # Collect checkpoints and certificates from all steps.
    checkpoints = []
    certificates = []
    for step_name in STEP_NAMES:
        if step_name in results:
            for checkpoint in results[step_name]["checkpoints"]:
                checkpoints.append((step_name, checkpoint))
            for certificate in results[step_name]["certificates"]:
                certificates.append((step_name, certificate))

    exceptions = []
    if "step02_small_n_and_baseline" in results:
        exceptions = results["step02_small_n_and_baseline"]["extra"].get("exceptions", [])

    open_cases = [c for (step, c) in certificates if c["certificate"]["type"] == "OPEN"]
    reducible_cases = [c for (step, c) in certificates if c["certificate"]["type"] == "REDUCIBLE"]
    different_checkpoints = [(step, c) for (step, c) in checkpoints if not c["matches"]]

    # ------------------------------------------------------------------------ 1. verdict
    computations_agree = (
        len(missing_steps) == 0
        and len(open_cases) == 0
        and len(reducible_cases) == 0
        and exceptions == EXPECTED_EXCEPTIONS
    )
    lines.append("## 1. Outcome")
    lines.append("")
    if computations_agree:
        lines.append("The computations agree with Theorem 1.1 of the paper: for %d < a <= %d the only"
                     % (A_MIN, A_MAX))
        lines.append("reducible L_n^(a) found are n = 2, a = m^2 - 2 with 8 <= m <= 31, and every finite")
        lines.append("case left by the filters is closed by a certificate.")
        lines.append("")
        lines.append("This is a personal re-run of the finite computations of the paper's proof, not an")
        lines.append("independent proof: the results listed in section 4 are taken as given.")
    else:
        lines.append("The computations do NOT (yet) agree with Theorem 1.1; see the list below.")
    lines.append("")
    lines.append("- steps not run yet: %s" % (missing_steps,))
    lines.append("- exceptions found (n, a): %s" % (exceptions,))
    lines.append("- cases left OPEN: %s" % ([(c["n"], c["a"], c["k"]) for c in open_cases],))
    lines.append("- REDUCIBLE cases among the certificates: %s" % ([(c["n"], c["a"], c["k"]) for c in reducible_cases],))
    lines.append("- checkpoints that differ from the paper: %d of %d" % (len(different_checkpoints), len(checkpoints)))
    lines.append("")

    # ---------------------------------------------------------------- 2. checkpoint table
    lines.append("## 2. Checkpoints (paper's value next to ours)")
    lines.append("")
    lines.append("| Step | Checkpoint | Paper | Ours | Match |")
    lines.append("| --- | --- | --- | --- | --- |")
    for (step_name, checkpoint) in checkpoints:
        lines.append("| %s | %s | %s | %s | %s |" % (
            step_name[:6],
            checkpoint["description"].replace("|", "/"),
            checkpoint["paper"],
            checkpoint["ours"],
            "yes" if checkpoint["matches"] else "NO",
        ))
    lines.append("")

    lines.append("### Differences and what we found")
    lines.append("")
    if len(different_checkpoints) == 0:
        lines.append("None.")
    for (step_name, checkpoint) in different_checkpoints:
        explanation = checkpoint.get("explanation", "")
        if explanation == "":
            explanation = "(no explanation recorded)"
        lines.append("- **%s, %s** %s" % (step_name[:6], checkpoint["description"], explanation))
    lines.append("")

    # ------------------------------------------------------------------- 3. certificates
    lines.append("## 3. Certificates")
    lines.append("")
    counts = {}
    for (step_name, certificate) in certificates:
        key = (step_name, certificate["certificate"]["type"])
        counts[key] = counts.get(key, 0) + 1
    lines.append("| Step | Certificate type | Number of cases |")
    lines.append("| --- | --- | --- |")
    for (step_name, certificate_type) in sorted(counts):
        lines.append("| %s | %s | %d |" % (step_name, certificate_type, counts[(step_name, certificate_type)]))
    lines.append("")
    lines.append("The individual certificates are in the results/*.json files.")
    lines.append("")

    # ------------------------------------------------------------------------ 4. imports
    lines.append("## 4. Imported results (assumed, not verified here)")
    lines.append("")
    for imported in IMPORTS:
        lines.append("- " + imported)
    lines.append("")

    text = "\n".join(lines)
    print(text)
    os.makedirs(RESULTS_DIRECTORY, exist_ok=True)
    summary_path = os.path.join(RESULTS_DIRECTORY, "summary.md")
    with open(summary_path, "w") as summary_file:
        summary_file.write(text)
    print("Saved %s" % summary_path)


if __name__ == "__main__":
    main()
