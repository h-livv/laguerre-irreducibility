# References

Bibliographic details are copied from the reference list of the paper being reproduced.
Numbers in square brackets are the numbers used there, and in the comments of this code.

## The paper being reproduced

- D. T. Das, S. Dutta, S. Laishram, S. G. Nair,
  *Irreducibility of Generalised Laguerre Polynomials for Large Integer Parameters*,
  [arXiv:2610.10614](https://arxiv.org/abs/2610.10614) (version 1, 7 October 2026).

All lemma, theorem, equation and table numbers in this repository refer to that version.
The theorem and its proof are the authors'. This repository only re-runs the proof's finite
computations.

## Results that the proof imports, and that this repository does not verify

| Used as | Reference | What is used |
| --- | --- | --- |
| Lemma 2.1 | [9] S. Laishram, T. N. Shorey, *The greatest prime divisor of a product of consecutive integers*, Acta Arith. 120 (2005), 299–306. | P(Δ(m−k+1, k)) > 2k (Theorem 1(a)) |
| Lemma 2.2 | [13] S. G. Nair, T. N. Shorey, *Lower bounds for the greatest prime factor of product of consecutive positive integers*, J. Number Theory (2015), 307–328. | P(Δ(m, k)) > 4.42k outside an explicit exception set (Theorem 2) |
| Lemma 2.3 | [15] F. Najman, *Large strings of consecutive smooth integers*, Arch. Math. 97 (2011), 319–324. | P(Δ(m, 6)) > 31 for m > 31, and > 37 for m > 37 |
| Lemma 2.10, and the range 0 ≤ a ≤ 50 | [10] S. Laishram, T. N. Shorey, *Extensions of Schur's irreducibility results*, Indag. Math. 21 (2011), 87–105. | the factor-exclusion criteria, and irreducibility for 0 ≤ a ≤ 50 with its exceptions |
| Størmer data (steps 4, 6, 7) | [11] D. H. Lehmer, *On a problem of Störmer*, Illinois J. Math. 8 (1964), 57–79. | Tables IA and IB: all m with P(m(m−1)) ≤ 31; none exceeds 1,611,308,700 |
| Lemma 6.4 | [21] G. Szegő, *Orthogonal Polynomials*, Amer. Math. Soc. Colloquium Publications, 1975. | bounds on the zeros of Laguerre polynomials (Theorems 6.31.2 and 6.31.3) |

## Classical tools that the code implements

| Used as | Reference | Where in the code |
| --- | --- | --- |
| Lemma 2.4 (Lucas) | [12] E. Lucas, *Théorie des fonctions numériques simplement périodiques*, Amer. J. Math. 1 (1878), 184–196. | tested in `tests/test_properties.py` |
| Lemma 2.5 (Legendre) | [8] H. Hasse, *Number Theory*, Classics in Mathematics, Springer, 2002 (Ch. 17, p. 263). | `factorial_valuation` in `laguerre/arithmetic.py` |
| Lemma 2.7 (Dumas) | [2] M. G. Dumas, *Sur quelques cas d'irréductibilité des polynômes à coefficients rationnels*, J. Math. Pures Appl. 2 (1906), 191–258. | `dumas_degree_set` in `laguerre/newton_polygon.py` |
| Lemma 2.8 (Filaseta) | [3] M. Filaseta, *The irreducibility of all but finitely many Bessel polynomials*, Acta Math. 174 (1995), 383–397 (Lemma 2). | `filaseta_excludes_degree` in `laguerre/newton_polygon.py` |

## Background mentioned in the paper

- [20] C. Störmer, *Quelques théorèmes sur l'équation de Pell x² − dy² = ±1 et leurs applications*,
  Skrifter Videnskabs-Selskabet i Christiania I (1897). (Finiteness of the m with P(m(m−1)) bounded.)
- [1] P. Banerjee, *An unsolved question surrounding the generalized Laguerre polynomial L_n^(n)(x)*,
  Ramanujan J. 65 (2024), 1147–1158. (The idea of bounding integer roots through Szegő's theory.)

## Software

- [SageMath](https://www.sagemath.org/), version 10.9: factorisation of polynomials over Q
  (`laguerre/oracles.py`). The paper also reports using SageMath for its computations.
- [mpmath](https://mpmath.org/): numerical roots in one property test.
- [pytest](https://pytest.org/): optional test runner.
