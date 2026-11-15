# Laguerre irreducibility for 50 < a ≤ 1000: a personal reproduction

This is a personal attempt to re-run the computational part of the proof of the main theorem of

> D. T. Das, S. Dutta, S. Laishram, S. G. Nair,
> *Irreducibility of Generalised Laguerre Polynomials for Large Integer Parameters*,
> [arXiv:2610.10614](https://arxiv.org/abs/2610.10614).

**The statement (Theorem 1.1 of the paper, on its new range).** For 50 < a ≤ 1000 and n ≥ 2,
the generalised Laguerre polynomial L_n^(a)(x) is irreducible over Q, except when n = 2 and
a + 2 is a perfect square (a = m² − 2, 8 ≤ m ≤ 31; 24 values). In those cases it has a
linear factor.

**What this repository is, and is not.**

- It is an independent, unofficial reproduction, written to understand the paper. It is not
  an artifact of the paper, and it has not been reviewed or endorsed by the paper's authors.
- It is **not an independent proof**. The theorem is the authors'. The code re-runs the finite
  computations of their proof and takes the lemmas that reduce the problem to those
  computations as given, together with several results from the literature
  (see ["What is imported, not verified"](#what-is-imported-not-verified)).
- The code has not been reviewed by anyone else. Where its numbers differ from the paper's,
  the cause may well be a misreading or a mistake on my side; the differences are reported
  as observations, not as corrections to the paper.

> **Status (run of 2026-11-14).** All steps ran and all 10 property tests pass. The
> computations agree with the theorem: the only reducible cases found are the 24 expected
> ones, and each of the 693 remaining finite cases was closed by an explicit computation.
> 72 of 78 intermediate values equal the ones printed in the paper; the 6 others are
> listed under ["Results"](#results). The whole run takes under a minute.

## The idea in one paragraph

A polynomial of degree n is reducible exactly when it has a factor of some degree k with
1 ≤ k ≤ n/2. The paper excludes such a factor for *every* n by a sieve:

1. **Filters.** Lemmas of the form "if there is a factor of degree k, then (n, a, k) satisfies
   this arithmetic condition" reduce "all n" to a finite list of cases (n, a, k).
2. **Certificates.** Each remaining case is closed by one explicit computation: a Newton
   polygon, a full factorisation, or an exhaustive search for integer roots.

We trust the proofs of the filter lemmas and re-run everything else: every count the paper
prints along the way is recomputed (a "checkpoint"), and every remaining case gets a stored
certificate.

## Requirements

- [SageMath](https://www.sagemath.org/) (developed against version 10.9, Python 3.14). It is
  used only to factorise polynomials. Everything else is plain Python with exact integers.
- `mpmath` (shipped with SageMath) is used by one property test.
- `pytest` is optional (the tests can also be run without it).

The easiest way to get all of this is the conda environment in `environment.yml`:

```bash
conda env create -f environment.yml      # or: mamba env create -f environment.yml
conda activate laguerre
export SAGE_PYTHON=python
```

`requirements.txt` lists the pure-Python packages only, for use inside an existing SageMath
installation. SageMath itself cannot be installed from it.

## How to run

The scripts must be run with **the Python interpreter that can `import sage`**. Below it is
called `$SAGE_PYTHON`. Which command that is depends on how Sage was installed:

| Sage installation | `$SAGE_PYTHON` |
| --- | --- |
| classic (source or binary) | `sage -python` |
| conda / mamba (the `sage` command then has no `-python` option) | the `python` inside the Sage environment: `python` once the environment is activated, or its full path, e.g. `/path/to/sage-env/bin/python` |

Set it once, then run from the repository root:

```bash
export SAGE_PYTHON="sage -python"                # or, with conda/mamba: export SAGE_PYTHON=python

bash run_all.sh                                  # everything, in order
```

or one step at a time:

```bash
$SAGE_PYTHON step01_newton_polygon_tables.py     # each step writes results/<step>.log and .json
...
$SAGE_PYTHON step09_assemble.py                  # writes results/summary.md
$SAGE_PYTHON -m pytest tests/ -v                 # property tests (or: $SAGE_PYTHON tests/test_properties.py)
```

The steps are independent of each other, except step 9, which only reads the result files.
Do them in order anyway: each one ends with checkpoints from the paper, and a later step is
hard to interpret while an earlier checkpoint disagrees.

## Where everything is

```
laguerre/                      the library (no script logic)
    config.py                  the range of a, limits, file locations
    arithmetic.py              ν_p, P(m), Rad(m), ω_p(m), Δ(m, l), the quantities of Section 4
    newton_polygon.py          Newton polygons, slopes φ_j, Dumas degree sets, Filaseta check
    oracles.py                 factorisation over Q; integer-root search; Proposition 1.3
    stormer.py                 smooth numbers; consecutive smooth numbers (Lehmer's table)
    filters.py                 one function per filter lemma: 2.10(i), 4.3, 5.1, 5.3, 5.4, 6.1, 6.2, 6.3
    certificates.py            builds the final proof record of one case (n, a, k)
    reporting.py               writes logs, checkpoints and certificates to results/
step01_ ... step09_ .py        one script per step (table below)
step11_deliverable_page.py     builds the one-page deliverable from the result files
tests/test_properties.py       step 10: property tests
REFERENCES.md                  the paper, the results it imports, and the software used
environment.yml                conda environment with SageMath (recommended way to install)
requirements.txt               the pure-Python packages, for an existing SageMath installation
data/lehmer_table_IA_p31.txt   optional typed copy of Lehmer's table (empty for now)
results/                       output of the scripts (empty until they are run)
run_all.sh                     runs all steps in order
```

| Step | Script | What it does | Paper |
| --- | --- | --- | --- |
| 1 | `step01_newton_polygon_tables.py` | recomputes the 8 Newton polygon tables | Lemmas 5.5, 5.6 |
| 2 | `step02_small_n_and_baseline.py` | n = 2 and n = 3; brute-force baseline for 4 ≤ n ≤ 30; spot-check of a ≤ 50 | Theorem 1.2 |
| 3 | `step03_lemma_2_6.py` | brute force over N ≤ 1005 | Lemma 2.6 |
| 4 | `step04_stormer_data.py` | all m with P(m(m−1)) ≤ 31, largest is n₂ = 1,611,308,700 | Lehmer's Table IA |
| 5 | `step05_k_at_least_6.py` | checks the numerical hypotheses of the (imported) argument for k ≥ 6 | Lemma 5.2 |
| 6 | `step06_k345_lemma_5_5.py` | sieve and certificates for k = 3, 4, 5 | Lemma 5.5 |
| 7 | `step07_k2_lemma_5_6.py` | sieve and certificates for k = 2 | Lemma 5.6 |
| 8 | `step08_k1_lemmas_6_5_6_6.py` | sieve and certificates for k = 1, n ≥ 4 | Lemmas 6.5, 6.6 |
| 9 | `step09_assemble.py` | combines all result files into `results/summary.md` | Theorem 1.1 |
| 10 | `tests/test_properties.py` | property tests | Lemmas 2.4, 2.5, 2.9, 4.1–4.3, 6.2, 6.4, Prop. 1.3 |
| 11 | `step11_deliverable_page.py` | builds the one-page deliverable `results/deliverable.html` from the result files | — |

## Vocabulary and conventions

- **The polynomial.** We always use the scaled polynomial 𝓛 = n!·L_n^(a)(x) = Σ (−1)^j a_j x^j
  with a_j = C(n, j)·(n+a)!/(j+a)!. It has integer coefficients, is monic up to sign, and has
  the same factor degrees as L_n^(a). In code, `a` is the parameter and `a_j` a coefficient.
- **Orientation of the Newton polygon.** The points are (n − j, ν_p(a_j)). So x = 0 is the
  leading coefficient and the right-most edge comes from the low-degree coefficients.
  `r1` is the horizontal length of the right-most edge.
- **Vertices and lattice points.** Vertices are the corners of the polygon. Lattice points
  also include integer points lying on the edges. The paper's tables mix the two; step 1
  accepts a table row if it contains all our vertices and only lattice points of our polygon.
- **Filter.** A function `lemma_X(n, a, k)` returning `(passes, reason)`. `passes = False`
  means the lemma proves there is no factor of degree k.
- **Checkpoint.** A value printed in the paper, recorded next to ours as MATCH or DIFFERENT.
  A difference never stops a script. A checkpoint can carry an explanation, which is shown
  in the log and in the summary when the values differ.
- **Certificate.** The record of the computation that closes one case. Its type is
  `newton_polygon`, `factorisation`, `root_search` or `dumas`; `OPEN` means not closed and
  `REDUCIBLE` means a factor of degree k exists.

## How to read the outcome

`results/summary.md` gives the outcome. The computations count as agreeing with the theorem
when all steps ran, no certificate is `OPEN` or `REDUCIBLE`, and the exceptions found are
exactly n = 2, a = m² − 2 (8 ≤ m ≤ 31).

A checkpoint that is DIFFERENT is not automatically a bug. The paper describes some filtering
stages loosely ("repeating the above process"), so the same proof can be organised with
different intermediate counts. The scripts are written so that the conclusion does not
depend on matching them: **every case that survives our filters is closed by a certificate**,
whatever the paper's count was. For each difference, first check which reading of the filter
gives the paper's number. What stays unexplained is an open question about how the paper's
count was obtained; it may equally come from a misreading here.

## Results

Full details are in `results/summary.md` (verdict, all 78 checkpoints, certificates) and in
the per-step `.log` and `.json` files.

**Outcome.** For 50 < a ≤ 1000 the only reducible L_n^(a) found are n = 2, a = m² − 2
(8 ≤ m ≤ 31), as the theorem states. The brute-force baseline (all 4 ≤ n ≤ 30) agrees.

**Certificates.**

| Branch | Cases closed | By Newton polygon | By factorisation | By root search |
| --- | --- | --- | --- | --- |
| n = 3 (step 2) | 12 | 0 | 12 | 0 |
| k = 3, 4, 5 (step 6) | 307 | 3 | 304 | 0 |
| k = 2 (step 7) | 58 | 51 | 7 | 0 |
| k = 1, n ≥ 4 (step 8) | 316 | 0 | 295 | 21 |

**The 6 checkpoints that differ from the paper.** None of them affects the theorem: all
cases that survive the filters here are closed by certificates, and every one of them turns
out irreducible. In rows 1–3 the lemmas, as I read them, leave a few cases that the paper's
text does not list. I do not know whether the paper removes them by a step it does not spell
out, or whether my reading of a lemma is too weak. Rows 5–6 are counts I could not reconstruct.

| # | Where | Paper | Ours | What we found |
| --- | --- | --- | --- | --- |
| 1 | Lemma 5.5: pairs (n, k) with P(Δ(n−k+1, k)) < 11 | n ≤ 10 and (16, 3) | also (50, 3) | 48·49·50 has largest prime 7, so (50, 3) also has P < 11, while the paper names (16, 3) as the only such pair with n ≥ 11. The paper's count 186 matches ours only without n = 50. Its 38 cases are closed here by factorisation. |
| 2 | Lemma 5.6: survivors with n = 81 | a = 115, 235, 544, 648 | also a = 144, 360 | Lemma 5.4 as stated does not eliminate these two. Both are closed by a Newton polygon (p = 3, slope 40/81). |
| 3 | Lemma 6.5: the set S̃ | 19 pairs | also (30, 699) | It passes Lemmas 6.1–6.3 and 5.4 as we read them, and no Newton polygon excludes it. Closed by factorisation (irreducible). |
| 4 | Lemma 6.5: (896, 979), candidates from Proposition 1.3 | ξ = 2770 | none | We also require Rad(n(n+a)) = 210 to divide ξ, which excludes 2770. Same conclusion. |
| 5 | Lemma 5.5: "97 distinct pairs (n, a)" | 97 | 228 | Unexplained. The 228 pairs for k = 3 are already distinct. |
| 6 | Lemma 6.5: "128 possible values of ξ" for (400, 624) | 128 | 270 | Unexplained. We count all multiples of 10 up to the bound 2706; other readings give 142, 124, 112, 94. |

**Two more findings that are not checkpoint differences.**

- *Lemma 6.6, the count 366.* It is reproduced exactly when the p = 3 condition of
  Lemma 5.4(ii) is NOT applied. With it, 296 pairs remain. The paper's six values of a for
  n = 512 do use the condition, but its list of 11 pairs with n > 300 does not: one of them,
  (768, 480), fails it. This also supports the reading of Lemma 6.1(iii) taken from the proof:
  the literal statement would remove (576, 482), which is in the paper's list.
- *Lemma 4.3, "r₂ ≠ p".* The proof only excludes alternative (c) of Lemma 4.1(ii), which is
  "r₂ = p and φ⁽²⁾ ≥ 1/k". As a statement about the Newton polygon alone, r₂ ≠ p fails: for
  (n, a, k, p) = (352, 845, 2, 11) we get r₁ = j₀ = 2, r₂ = 11, φ⁽²⁾ = 1/9. Nothing
  downstream depends on it. The property test checks the version that the proof shows.

## Readings of the paper used in the code

These are the places where the printed text is ambiguous. Each is also documented in the
docstring of the function concerned.

| Place | Reading used |
| --- | --- |
| Lemma 5.3, second condition | p² ∥ Δ(a+k−⌈k/2⌉+1, ⌈k/2⌉). (Text extraction of the PDF loses the square.) |
| Lemma 5.3, k = 2, p = 7 | 7² \| (a+2) or 7³ ∥ (a+4); the extra "p ∥ n(n−1)" is not used, as in the paper's own count 13 × 21 = 273. |
| Lemma 5.5, set T̃ | all n of the first list with 11·19 \| Δ(n−4, 5) for a = 358, and 11·13 \| Δ(n−4, 5) for a = 842. |
| Lemma 5.5, "prime divisor of Δ(n+a−k+1, k)" | read as Δ(n−k+1, k), which is what Lemma 5.3 is about. |
| Lemma 5.4(ii), p = 3, "r₁ < 12" | some 1 ≤ j ≤ 11 satisfies ν₃(Δ(a+1, j)) − ν₃(C(n, j)) ≥ j (equation (15)). |
| Lemma 6.1(ii) | j = 1: p² \| (a+1), ν_p(n) ≤ ν_p(a+1) − 1; j ≥ 2: p^(j+1) \| (a+j), ν_p(n) = ν_p(a+j) − j. |
| Lemma 6.1(iii), 3 ∥ (a+1) | the two inequalities are joined by "or" (as in the proof), not "and" (as in the statement). |
| Lemma 6.1(iii), 3³ \| (a+2) | ν₃(n) ≤ ν₃(a+2) − 2 (the union of the cases of the proof), not "=" (as in the statement). |
| Lemmas 6.5, 6.6, the use of Proposition 1.3 | candidates ξ are found by looping over the multiples of Rad(n(n+a)) up to the Szegő bound and keeping those that satisfy equations (19) and (20). Formula (1) and the bound d₁d₂ > (n−1)/6 follow from these. |
| Lemma 6.5, "128 possible values of ξ" for (400, 624) | not clear how they are counted; we report the number of multiples of Rad(n(n+a)) in (0, B]. |
| Lemma 6.6, the count 366 | counted without the p = 3 condition of Lemma 5.4(ii) (this reading gives exactly 366). Our certificates use the full lemma. |
| Lemma 4.3, "r₂ ≠ p" | "alternative (c) of Lemma 4.1(ii) does not occur" (see Results). |
| "1 ≤ k ≤ 2n" in Lemmas 2.9 and 4.1 | 1 ≤ k ≤ n/2. |

In the two places of Lemma 6.1(iii) we use the weaker condition. A weaker filter keeps more
cases, which then need certificates; it can never wrongly eliminate a case.

## What is imported, not verified

Full bibliographic details are in [`REFERENCES.md`](REFERENCES.md).
The reproduction assumes the following results. `step09_assemble.py` prints this list in the
summary so that it is never presented as verified.

- Lemma 2.1 (Laishram–Shorey), Lemma 2.2 (Nair–Shorey), Lemma 2.3 (Najman), Lemma 2.10
  (Laishram–Shorey), and the deduction of Lemma 5.2 from them (no factor of degree k ≥ 6).
- Lehmer's Tables IA and IB: there is no m > 1,611,308,700 with P(m(m−1)) ≤ 31. Our
  enumeration reproduces the table up to 10¹⁰ but cannot prove that nothing lies beyond.
- Szegő's bounds on the zeros (Lemma 6.4).
- The whole range 0 ≤ a ≤ 50 (Laishram–Shorey). Only its exceptions are spot-checked.
- The proofs of the filter lemmas 4.1–4.3, 5.1, 5.3, 5.4, 6.1–6.3 and of Proposition 1.3.

The baseline of step 2 (factorising all 4 ≤ n ≤ 30) is an independent check of the result,
not part of the proof: only the sieve covers all n.

## Changing the range of a

`A_MIN` and `A_MAX` in `laguerre/config.py` set the range of a in every script. But several
lemmas contain numbers that the paper derives from a ≤ 1000 (the primes 31 and 37, the
exponent bounds of Lemmas 6.1 and 6.3, the bound N ≤ 1005 of Lemma 2.6, Lehmer's table for
the prime 31). They are marked in `config.py` and in the docstrings of `filters.py`. With a
larger `A_MAX` those lemmas are no longer proved; such a run only shows where the method breaks.

## Not done

- **Typed copy of Lehmer's Table IA** (`data/lehmer_table_IA_p31.txt` is empty). Step 4 compares
  it with the recomputed table once it is typed in.
- **Optional Dumas grid for k ≥ 6** (not needed for the proof). `dumas_degree_set`
  in `laguerre/newton_polygon.py` is the function to use for it.
