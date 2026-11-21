# Extension: Laguerre irreducibility for 1000 < a <= 1078

## 1. Outcome

For 1000 < a <= 1078 and n >= 2, the computations of the paper's proof go through unchanged: the only reducible L_n^(a) are n = 2, a + 2 a perfect square, that is a = [1022].

- largest A allowed by the audit: 1078 (binding: Lemma 4.3: c0 = 2 for every prime p >= 11 (eq. (6): a + p + p^2 <= (p-1)p^2))
- exceptions found (n, a): [[2, 1022]] (expected [[2, 1022]])
- cases left OPEN: []
- REDUCIBLE cases among the certificates: []
- brute-force baseline 4 <= n <= 30, reducible pairs: [[]]

## 2. Audit: where the proof uses a <= 1000

| Statement | Holds for all a <= A, largest A | Holds at A = 1078 |
| --- | --- | --- |
| Lemma 4.3: c0 = 2 for every prime p >= 11 (eq. (6): a + p + p^2 <= (p-1)p^2) | 1078 | yes |
| Lemma 6.3(i): 7^2 * 5^2 > a + 1 and 5^2 * 11^2 > a + 1 | 1223 | yes |
| Lemma 5.4, table: v~ <= 2 for p >= 11 (p^3 > a + 3(p-1)) | 1300 | yes |
| Lemma 5.4(iii): no p >= 11 with p^3 | a + j, j <= 5 | 1325 | yes |
| Lemma 6.3(iii): p^2 q > a + 1 for p, q >= 11 | 1329 | yes |
| Lemma 5.1: a + p < p^2 for p >= 37 | 1331 | yes |
| Lemma 5.4(i): nu_p(Delta(a+1, p)) = 1 for p >= 37 | 1331 | yes |
| Lemma 5.4, table: v~ <= 1 for p >= 37 (p^2 > a + r1, r1 < p) | 1332 | yes |
| Lemma 2.6, N <= a + 5: no solutions beyond the paper's two | 1439 | yes |
| Lemma 6.1(iii): c0 <= 6 and v0 <= 6 for p = 3 | 1446 | yes |
| Lemma 5.2: p^2 - p >= a for the primes p >= 41 used with Lemma 2.10(i) | 1640 | yes |
| Lemma 5.3, k = 2, p = 7: c0 = 3 (taken in the proof) | 2002 | yes |
| Lemma 5.4, table: v~ <= 6 for p = 3 (3^7 > a + 7*2) | 2172 | yes |
| Lemma 6.1(iii), v0 = 1: 3^v - a < 2v forces v <= 6 | 2173 | yes |
| Lemma 5.4, table: v~ <= 3 for p = 7 (7^4 > a + 4*6) | 2376 | yes |
| Lemma 5.3, k = 2, p = 7: 7^4 > a + 4, so 7^3 || (a+2)(a+4) | 2396 | yes |
| Lemma 6.3(i): 7^3 | (a+2) is incompatible with Lemma 6.1(ii) for p = 5 | 2398 | yes |
| Lemma 6.1(ii): c0 <= p - 1 for p = 5 and p = 7 | 2470 | yes |
| Lemma 5.4, table: v~ <= 4 for p = 5 (5^5 > a + 5*4) | 3104 | yes |
| Lemma 4.2: p^v0 <= a + p < p^5 for p >= 5, so v0 <= 4 | 3119 | yes |
| Lemma 5.3, k = 2, p = 7: no q > 7 with q^2 | (a+2) when 7^3 | (a+4) | 4111 | yes |
| Lemma 5.2: the window n <= M(k) - 1 contradicts p > 4.42k for all 18 <= k < a/5 | >= 5000 | yes |
| Lemma 5.3, k = 2, p = 7: p^2 q^2 > a + 2 for primes 7 <= p < q | >= 5000 | yes |

## 3. Certificates

| Step | Certificate type | Number of cases |
| --- | --- | --- |
| step02_small_n_and_baseline | factorisation | 1 |
| step08_k1_lemmas_6_5_6_6 | factorisation | 14 |
| step08_k1_lemmas_6_5_6_6 | root_search | 8 |

The per-step logs and certificates are in this folder. The counts logged as COUNT
are for the new range only; the paper's values (for a <= 1000) do not apply to them.

## 4. Assumed, not verified

The same imports as the a <= 1000 reproduction (see ../summary.md, section 4), and the
proofs of the filter lemmas, read with a <= 1078 in place of a <= 1000. Section 2 lists
every place where those proofs use the bound on a.
