# Extension: Laguerre irreducibility for 1000 < a ≤ 1078

**Result.** The proof of Theorem 1.1 in Das–Dutta–Laishram–Nair
([arXiv:2610.10614](https://arxiv.org/abs/2610.10614)) extends unchanged to **a ≤ 1078**.
For 1000 < a ≤ 1078 and n ≥ 2, L_n^(a)(x) is irreducible over Q except for one new case:
n = 2, a = 1022, where a + 2 = 32² gives a linear factor.

Combined with Theorem 1.1, for 0 ≤ a ≤ 1078 the exceptions are n = 2 with a + 2 = m²
(2 ≤ m ≤ 32), and (n, a) = (4, 5), (4, 23).

This is not an independent proof. It rests on the same assumptions as the a ≤ 1000
reproduction (see [DOCUMENTATION.md](DOCUMENTATION.md#what-is-imported-not-verified)): the imported results
of the literature and the proofs of the filter lemmas. Here those proofs are read with
a ≤ 1078 in place of a ≤ 1000, and every place where they use the bound was checked.

Run of 2026-11-21. Code: [`extension_a1078.py`](extension_a1078.py). Output:
[`results/extension_a1078/`](results/extension_a1078/).

## Where a ≤ 1000 enters the proof

The binding constraint is **Lemma 4.3 at p = 11**. Its proof needs c₀ = 2 in equation (6),
that is a + p + p² ≤ (p − 1)p². At p = 11 this reads a + 132 ≤ 1210, so a ≤ 1078.
Lemmas 5.1 and 5.3 rest on Lemma 4.3, so the whole k ≤ 5 sieve stops there.

The script writes each use of a ≤ 1000 in the proofs as an inequality in a bound A. It then
scans A upward to find the largest value for which the inequality holds for every a ≤ A.
There are 23 statements. The six tightest:

| Statement (paper) | Holds for all a ≤ |
| --- | --- |
| Lemma 4.3: c₀ = 2 for every prime p ≥ 11 | **1078** |
| Lemma 6.3(i): 7²·5² > a + 1 | 1223 |
| Lemma 5.4 table: ṽ ≤ 2 for p ≥ 11 (11³ > a + 30) | 1300 |
| Lemma 5.4(iii): no p ≥ 11 with p³ \| a + j, j ≤ 5 | 1325 |
| Lemma 6.3(iii): p²q > a + 1 for p, q ≥ 11 | 1329 |
| Lemma 5.1: a + p < p² for p ≥ 37 | 1331 |

The other 17 hold at least to a = 1331. They include the recomputation of Lemma 2.6 for
N ≤ a + 5: its only solutions remain the paper's (363, 11, 19) and (847, 11, 13), so the
exceptional set T̃ of Lemma 5.5 gains nothing. The full table is in
[`results/extension_a1078/summary.md`](results/extension_a1078/summary.md).

## The sieve on 1000 < a ≤ 1078

The filter lemmas leave 23 cases across the 78 new values of a. Each one is closed by an
explicit computation, and only the expected n = 2 case is reducible.

| Degree of the factor | Cases left by the filters | How they were closed |
| --- | --- | --- |
| n = 2 | a + 2 square: a = 1022 | factorisation: **reducible** (the new exception) |
| n = 3 | Theorem 1.2(ii): a = 1021 | factorisation: irreducible |
| k ≥ 6 | none (Lemma 5.2, no computation) | numerical hypotheses checked (see below) |
| k = 3, 4, 5 | 30 triples after Lemma 5.3 (16 / 8 / 6); none from the small-n pairs | all removed by Lemma 5.4(i) |
| k = 2 | 59 values of n, then the pairs from Lemma 5.3 | all removed by Lemma 5.4(i) and (iii) |
| k = 1, P(n) ≥ 5 | 3 pairs: (1280, 1024), (5120, 1024), (15360, 1024) | integer-root search: no root |
| k = 1, n = 2^α·3^β | 19 pairs | 14 by factorisation (n ≤ 256); 5 by root search: (512, 1024), (512, 1056), (1024, 1024), (1536, 1024), (3072, 1024) |

As an independent cross-check, every 4 ≤ n ≤ 30 was factorised directly for every new a.
None is reducible.

One value stands out. 9 of the 22 linear-factor survivors with n ≥ 4 have a = 1024 = 2¹⁰,
among them all three with P(n) ≥ 5 and every n above 512. At a = 1024, Lemma 6.3(ii) first
allows ν₂(n) = 10, and no lemma restricts the prime 2 further.

## What changed from the a ≤ 1000 argument

- **1078, not 1077.** The proof of Lemma 4.3 writes the strict inequality
  "1000 + p + p² < (p − 1)p²", which would give 1077. The definition of c₀ in (6) uses ≤,
  and at a = 1078 Remark 1(i) still gives t₀ ≤ 9, so ν₁₁(t₀ + 1) = 0. The two readings differ
  only at a = 1078.
- **Lemma 5.2 needs a small repair.** The proof says max(2k + 13, 541k/262) = 2k + 13
  "since k < 200". With a ≤ 1078, k can reach 215, and the identity fails for k ≥ 201. The
  argument still closes: Lemma 2.1 gives n ≤ max(2k + 13, ⌈541k/262⌉) − 1 ≤ 2k + 13, which
  stays below the prime p > 4.42k from Lemma 2.2. The script checks this for 18 ≤ k ≤ 215.
- **New special values of a, handled by the existing proofs.**
  In Lemma 5.3 (k = 2, p = 7), 7³ | (a + 4) now also allows a = 1025; a + 2 = 1027 = 13·79
  has no square factor, as the argument needs. In Lemma 6.3(i), 7³ | (a + 2) now also allows
  a = 1027; none of 5² | a + 1, 5³ | a + 2, 5⁴ | a + 3 holds, as the argument needs.
- **Lemma 6.3(ii): α ≤ 10 instead of 9** once a ≥ 1024. The code already tests
  2^ν₂(n) ≤ a, so nothing had to change.

## Going further

At a = 1079 the argument breaks, not the theorem: c₀ becomes 3 for p = 11 and stays 3 up to
a = 1846. Lemma 4.1 then needs (c − 1)(11^v₀ + 11)/10 ≥ 3. When v₀ = 1 this forces c ≥ 3,
so 11 ≥ 1 + 3k, which covers only k ≤ 3. Reaching past 1078 means reproving Lemma 4.3 for
p = 11 with c₀ = 3, with a separate argument for k = 4 and 5.

Even with that repair, the next limits come soon. Lemma 6.3(i) fails at a = 1224; Lemma 5.4
and Lemma 6.3(iii) need 11³ > a + small, which fails between a = 1301 and 1330; Lemma 5.1
fails at a = 1332. Past 1331 the smoothness bound rises from 31 to 37, and the k = 2 to 5
sieves would need Lehmer's table for the prime 37. So the next realistic target is
a ≤ 1223, which needs only the Lemma 4.3 repair.

- [ ] Reprove Lemma 4.3 for p = 11, c₀ = 3 (1079 ≤ a ≤ 1846)
- [ ] Past 1223: rework Lemma 6.3(i) for 7²·5² | a + 1
- [ ] Rerun `extension_a1078.py` with the new bound once both hold

## Reproducing

```bash
$SAGE_PYTHON extension_a1078.py          # about 15 seconds
```

1. **Audit.** Computes the largest A for each of the 23 a-dependent statements, and stops
   if any is below 1078.
2. **Sieve.** Reruns steps 2, 6, 7 and 8 of the reproduction on 1000 < a ≤ 1078 only, with
   the same filter and certificate code. The paper's checkpoint values apply to a ≤ 1000,
   so these steps log plain counts (`COUNT`) instead.
3. **Summary.** Writes `results/extension_a1078/summary.md` and `audit.json`, next to the
   per-step logs and certificates.

The library and the a ≤ 1000 results are not modified.

Notes on the logs: step 6 still carries the set T̃ (a ∈ {358, 842}), which lies outside the
new range; Lemma 5.4(i) removes those triples. Step 8 still recomputes the three root
searches that the paper describes for a ≤ 1000, for comparison only.
