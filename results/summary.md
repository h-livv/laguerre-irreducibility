# Summary: Laguerre irreducibility for 50 < a <= 1000

## 1. Outcome

The computations agree with Theorem 1.1 of the paper: for 50 < a <= 1000 the only
reducible L_n^(a) found are n = 2, a = m^2 - 2 with 8 <= m <= 31, and every finite
case left by the filters is closed by a certificate.

This is a personal re-run of the finite computations of the paper's proof, not an
independent proof: the results listed in section 4 are taken as given.

- steps not run yet: []
- exceptions found (n, a): [[2, 62], [2, 79], [2, 98], [2, 119], [2, 142], [2, 167], [2, 194], [2, 223], [2, 254], [2, 287], [2, 322], [2, 359], [2, 398], [2, 439], [2, 482], [2, 527], [2, 574], [2, 623], [2, 674], [2, 727], [2, 782], [2, 839], [2, 898], [2, 959]]
- cases left OPEN: []
- REDUCIBLE cases among the certificates: []
- checkpoints that differ from the paper: 6 of 78

## 2. Checkpoints (paper's value next to ours)

| Step | Checkpoint | Paper | Ours | Match |
| --- | --- | --- | --- | --- |
| step01 | Table row (25, 527, 3), p = 29: paper's points agree with our polygon | True | True | yes |
| step01 | Table row (25, 527, 3), p = 29: slope of the right-most edge | 1/24 | 1/24 | yes |
| step01 | Table row (25, 527, 3), p = 29: Lemma 2.8 excludes degree k | True | True | yes |
| step01 | Table row (56, 845, 3), p = 17: paper's points agree with our polygon | True | True | yes |
| step01 | Table row (56, 845, 3), p = 17: slope of the right-most edge | 1/5 | 1/5 | yes |
| step01 | Table row (56, 845, 3), p = 17: Lemma 2.8 excludes degree k | True | True | yes |
| step01 | Table row (65, 167, 3), p = 29: paper's points agree with our polygon | True | True | yes |
| step01 | Table row (65, 167, 3), p = 29: slope of the right-most edge | 1/7 | 1/7 | yes |
| step01 | Table row (65, 167, 3), p = 29: Lemma 2.8 excludes degree k | True | True | yes |
| step01 | Table row (36, 339, 2), p = 3: paper's points agree with our polygon | True | True | yes |
| step01 | Table row (36, 339, 2), p = 3: slope of the right-most edge | 13/27 | 13/27 | yes |
| step01 | Table row (36, 339, 2), p = 3: Lemma 2.8 excludes degree k | True | True | yes |
| step01 | Table row (81, 115, 2), p = 7: paper's points agree with our polygon | True | True | yes |
| step01 | Table row (81, 115, 2), p = 7: slope of the right-most edge | 1/4 | 1/4 | yes |
| step01 | Table row (81, 115, 2), p = 7: Lemma 2.8 excludes degree k | True | True | yes |
| step01 | Table row (81, 235, 2), p = 7: paper's points agree with our polygon | True | True | yes |
| step01 | Table row (81, 235, 2), p = 7: slope of the right-most edge | 1/3 | 1/3 | yes |
| step01 | Table row (81, 235, 2), p = 7: Lemma 2.8 excludes degree k | True | True | yes |
| step01 | Table row (81, 544, 2), p = 3: paper's points agree with our polygon | True | True | yes |
| step01 | Table row (81, 544, 2), p = 3: slope of the right-most edge | 40/81 | 40/81 | yes |
| step01 | Table row (81, 544, 2), p = 3: Lemma 2.8 excludes degree k | True | True | yes |
| step01 | Table row (81, 648, 2), p = 7: paper's points agree with our polygon | True | True | yes |
| step01 | Table row (81, 648, 2), p = 7: slope of the right-most edge | 1/3 | 1/3 | yes |
| step01 | Table row (81, 648, 2), p = 7: Lemma 2.8 excludes degree k | True | True | yes |
| step02 | n = 2: the a with L_2^(a) reducible (by factorisation) | [62, 79, 98, 119, 142, 167, 194, 223, 254, 287, 322, 359, 398, 439, 482, 527, 574, 623, 674, 727, 782, 839, 898, 959] | [62, 79, 98, 119, 142, 167, 194, 223, 254, 287, 322, 359, 398, 439, 482, 527, 574, 623, 674, 727, 782, 839, 898, 959] | yes |
| step02 | n = 2: Theorem 1.2(i), reducible exactly when a + 2 is a square | [62, 79, 98, 119, 142, 167, 194, 223, 254, 287, 322, 359, 398, 439, 482, 527, 574, 623, 674, 727, 782, 839, 898, 959] | [62, 79, 98, 119, 142, 167, 194, 223, 254, 287, 322, 359, 398, 439, 482, 527, 574, 623, 674, 727, 782, 839, 898, 959] | yes |
| step02 | n = 3: the a allowed by Theorem 1.2(ii) | [51, 105, 122, 125, 247, 253, 340, 429, 497, 683, 726, 861] | [51, 105, 122, 125, 247, 253, 340, 429, 497, 683, 726, 861] | yes |
| step02 | n = 3: the a with L_3^(a) reducible (by factorisation) | [] | [] | yes |
| step02 | n = 3: every reducible L_3^(a) has the shape of Theorem 1.2(ii) | True | True | yes |
| step02 | baseline: reducible (n, a) with 4 <= n <= 30 | [] | [] | yes |
| step02 | imported exceptions (a <= 50) that have a linear factor | [[2, 2], [2, 7], [2, 14], [2, 23], [2, 34], [2, 47], [4, 5], [4, 23]] | [[2, 2], [2, 7], [2, 14], [2, 23], [2, 34], [2, 47], [4, 5], [4, 23]] | yes |
| step03 | Lemma 2.6(i): triples (N, p, q) | [] | [] | yes |
| step03 | Lemma 2.6(ii): triples (N, p, q) | [[363, 11, 19], [847, 11, 13]] | [[363, 11, 19], [847, 11, 13]] | yes |
| step03 | Lemma 2.6(iii): pairs (N, p) | [] | [] | yes |
| step04 | largest m <= 10^10 with P(m(m-1)) <= 31 (Lehmer's n_2) | 1611308700 | 1611308700 | yes |
| step05 | largest k with 5k < a <= 1000 (the paper says k < 200) | 199 | 199 | yes |
| step05 | for 6 <= k <= 199: max(2k+13, 541k/262) = 2k+13 | True | True | yes |
| step05 | for k >= 18: max(1+2k, 37) = 1+2k | True | True | yes |
| step05 | for k >= 18: 4.42k >= 37 | True | True | yes |
| step05 | the exception set T of Lemma 2.2 has no k >= 18 | True | True | yes |
| step05 | p^2 - p >= 1000 for the first prime p = 41 above 37 | True | True | yes |
| step05 | for 6 <= k < 18: max(1+2k, 37) = 37 | True | True | yes |
| step05 | for 6 <= k < 18: 6k+1 >= 37 | True | True | yes |
| step06 | Stage A: number of n with P(Delta(n-k+1,k)) <= 31, n >= 2k, for k = 3, 4, 5 | [87, 46, 31] | [87, 46, 31] | yes |
| step06 | Stage B: the set T-tilde | [[13, 842, 5], [14, 842, 5], [15, 842, 5], [22, 358, 5], [23, 358, 5], [26, 842, 5], [58, 358, 5], [66, 842, 5], [156, 358, 5], [156, 842, 5]] | [[13, 842, 5], [14, 842, 5], [15, 842, 5], [22, 358, 5], [23, 358, 5], [26, 842, 5], [58, 358, 5], [66, 842, 5], [156, 358, 5], [156, 842, 5]] | yes |
| step06 | Stage C: number of n after omega_11 <= 1 and nu_p <= 1, for k = 3, 4, 5 | [31, 14, 6] | [31, 14, 6] | yes |
| step06 | Stage D: pairs (n, k) with P(Delta(n-k+1,k)) < 11 | [[6, 3], [7, 3], [8, 3], [8, 4], [9, 3], [9, 4], [10, 3], [10, 4], [10, 5], [16, 3]] | [[6, 3], [7, 3], [8, 3], [8, 4], [9, 3], [9, 4], [10, 3], [10, 4], [10, 5], [16, 3], [50, 3]] | NO |
| step06 | Stage D: number of pairs (n, a) after Lemma 5.3, for k = 3, 4, 5 | [186, 96, 87] | [186, 96, 87] | yes |
| step06 | Stage D: number of triples including T-tilde | 379 | 379 | yes |
| step06 | Stage E: triples with P(Delta(n+a-k+1,k)) < 37 | [[25, 527, 3], [65, 167, 3]] | [[25, 527, 3], [65, 167, 3]] | yes |
| step06 | Stage E: survivors of Lemma 5.4(i) | [[25, 527, 3], [56, 845, 3], [65, 167, 3]] | [[25, 527, 3], [56, 845, 3], [65, 167, 3]] | yes |
| step06 | Stage F: number of pairs (n, a) for the paper's small pairs, for k = 3, 4, 5 | [228, 36, 2] | [228, 36, 2] | yes |
| step06 | Stage F: number of distinct (n, a) for the paper's small pairs | 97 | 228 | NO |
| step07 | Stage A: largest n with P(n(n-1)) <= 31 (Lehmer's n_2) | 1611308700 | 1611308700 | yes |
| step07 | Stage B: every n > 10^5 has omega_11(n(n-1)) >= 2 (Lehmer's Table IB) | True | True | yes |
| step07 | Stage B: number of n with P(n(n-1)) <= 31 and omega_7(n(n-1)) <= 1 | 59 | 59 | yes |
| step07 | Stage B: all these n are <= 10^5 | True | True | yes |
| step07 | Stage C, group 11 to 31: [number of n, number of pairs] | [32, 118] | [32, 118] | yes |
| step07 | Stage C, group 7: [number of n, number of a, number of pairs] | [13, 21, 273] | [13, 21, 273] | yes |
| step07 | Stage C, group at most 5: the values of n | [4, 5, 6, 9, 10, 16, 25, 81] | [4, 5, 6, 9, 10, 16, 25, 81] | yes |
| step07 | Stage D, group 11 to 31: P((n+a)(n+a-1)) >= 11 for all pairs | True | True | yes |
| step07 | Stage D, group 11 to 31: pairs with P((n+a)(n+a-1)) >= 37, and <= 31 | [106, 12] | [106, 12] | yes |
| step07 | Stage D, group 11 to 31: of these, P((n+a)(n+a-1)) <= P((n-3)(n-2)) | 8 | 8 | yes |
| step07 | Stage D, group 11 to 31: pairs with P >= 37 passing Lemma 5.4(i) | [] | [] | yes |
| step07 | Stage D, group 11 to 31: pairs with P <= 31 passing Lemma 5.4(iii) | [] | [] | yes |
| step07 | Stage D, group 11 to 31: survivors | [] | [] | yes |
| step07 | Stage D, group 7: survivors | [[36, 339]] | [[36, 339]] | yes |
| step07 | Stage D, group at most 5: survivors with n = 81 | [[81, 115], [81, 235], [81, 544], [81, 648]] | [[81, 115], [81, 144], [81, 235], [81, 360], [81, 544], [81, 648]] | NO |
| step07 | Stage D, group at most 5: number of survivors with n != 81 | 51 | 51 | yes |
| step08 | Part A: pairs with 11 <= P(n) <= 31 before Lemma 5.4 | 17 | 17 | yes |
| step08 | Part A: pairs with 11 <= P(n) <= 31 after Lemma 5.4 | [[22, 362], [152, 360], [6656, 844]] | [[22, 362], [152, 360], [6656, 844]] | yes |
| step08 | Part A: the set S-tilde | [[5, 123], [5, 724], [10, 374], [20, 124], [22, 362], [25, 623], [25, 999], [40, 248], [40, 824], [40, 974], [56, 538], [152, 360], [160, 224], [200, 124], [320, 724], [400, 624], [640, 224], [896, 979], [6656, 844]] | [[5, 123], [5, 724], [10, 374], [20, 124], [22, 362], [25, 623], [25, 999], [30, 699], [40, 248], [40, 824], [40, 974], [56, 538], [152, 360], [160, 224], [200, 124], [320, 724], [400, 624], [640, 224], [896, 979], [6656, 844]] | NO |
| step08 | Part B: number of pairs, without the p = 3 condition of Lemma 5.4(ii) | 366 | 366 | yes |
| step08 | Part B: pairs with n > 300 and n != 512, without the p = 3 condition | [[384, 480], [432, 80], [576, 160], [576, 482], [576, 674], [768, 294], [768, 480], [768, 584], [768, 753], [1152, 723], [1536, 512]] | [[384, 480], [432, 80], [576, 160], [576, 482], [576, 674], [768, 294], [768, 480], [768, 584], [768, 753], [1152, 723], [1536, 512]] | yes |
| step08 | Part B: the values of a for n = 512, with the p = 3 condition | [512, 576, 656, 664, 860, 948] | [512, 576, 656, 664, 860, 948] | yes |
| step08 | (n, a) = (896, 979): candidates left by Proposition 1.3 (paper: xi = 2770, not a root) | [2770] | [] | NO |
| step08 | (n, a) = (512, 512): candidates left by Proposition 1.3 (paper: xi = 2046, not a root) | [2046] | [2046] | yes |
| step08 | (n, a) = (400, 624): number of candidate xi checked (reading uncertain) | 128 | 270 | NO |

### Differences and what we found

- **step06, Stage D: pairs (n, k) with P(Delta(n-k+1,k)) < 11** The paper says P(Delta(n-k+1,k)) >= 11 for all n >= 11 except (16, 3). But (n, k) = (50, 3) gives 48 * 49 * 50, whose largest prime is 7. The paper's count 186 for k = 3 matches ours only without n = 50, so this pair does not seem to be covered by the paper's counts. It is treated here in Stage F like the other small pairs (38 extra cases, all closed by factorisation).
- **step06, Stage F: number of distinct (n, a) for the paper's small pairs** UNEXPLAINED. The 228 pairs for k = 3 are already distinct, so the number of distinct (n, a) cannot be below 228. We factorise all of them, so nothing is lost.
- **step07, Stage D, group at most 5: survivors with n = 81** Lemma 5.4 as stated does not eliminate a = 144 and a = 360: 225 * 224 has no prime >= 11, and for 441 * 440 the prime 11 satisfies 11^2 | (a + 3). The paper does not say how it removes them. Both are closed below by a Newton polygon (p = 3, right-most slope 40/81 < 1/2).
- **step08, Part A: the set S-tilde** We get one extra pair, (30, 699). It passes Lemmas 6.1, 6.2, 6.3 and 5.4 as we read them: 5^2 | (a+1), 3^3 | (a+3) with nu_3(n) = 1, and n + a = 3^6. No Newton polygon excludes it either (the right-most slope is >= 1 for p = 2, 3, 5). It is closed by factorisation: the polynomial is irreducible.
- **step08, (n, a) = (896, 979): candidates left by Proposition 1.3 (paper: xi = 2770, not a root)** Our candidate list also requires Rad(n(n+a)) | xi (Remark 2 of the paper). Here Rad(896 * 1875) = 210 does not divide 2770, so 2770 is already excluded and no candidate is left. The conclusion (no integer root) is the same.
- **step08, (n, a) = (400, 624): number of candidate xi checked (reading uncertain)** UNEXPLAINED. We count all multiples of Rad(n(n+a)) = 10 in (0, 2706]. Other readings we tried give 142 (xi sharing a factor with (n-1)(n+a-1)), 124, 112 and 94. All 270 candidates are tested and none is a root, so nothing is lost.

## 3. Certificates

| Step | Certificate type | Number of cases |
| --- | --- | --- |
| step02_small_n_and_baseline | factorisation | 12 |
| step06_k345_lemma_5_5 | factorisation | 304 |
| step06_k345_lemma_5_5 | newton_polygon | 3 |
| step07_k2_lemma_5_6 | factorisation | 7 |
| step07_k2_lemma_5_6 | newton_polygon | 51 |
| step08_k1_lemmas_6_5_6_6 | factorisation | 295 |
| step08_k1_lemmas_6_5_6_6 | root_search | 21 |

The individual certificates are in the results/*.json files.

## 4. Imported results (assumed, not verified here)

- Lemma 2.1 (Laishram-Shorey 2005): P(Delta(m-k+1, k)) > 2k.
- Lemma 2.2 (Nair-Shorey 2015): P(Delta(m, k)) > 4.42k outside the exception set T.
- Lemma 2.3 (Najman 2011): P(Delta(m, 6)) > 31 for m > 31, and > 37 for m > 37.
- Lemma 2.10 (Laishram-Shorey 2011): the prime criterion (i) and the range a <= 5k (ii).
- Lemma 5.2: the deduction that there is no factor of degree k >= 6 (hypotheses checked in step 5).
- Lehmer 1964, Tables IA and IB: no m > 1,611,308,700 has P(m(m-1)) <= 31.
- Szego, Theorems 6.31.2-3: the bounds on the zeros of Laguerre polynomials (Lemma 6.4).
- Laishram-Shorey 2011, Theorem 1: the whole range 0 <= a <= 50.
- The proofs of the filter lemmas 4.1-4.3, 5.1, 5.3, 5.4, 6.1-6.3 and of Proposition 1.3.
