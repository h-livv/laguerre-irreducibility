# Laguerre irreducibility for 50 < a ≤ 1078

A personal, unofficial reproduction of the computations in

> D. T. Das, S. Dutta, S. Laishram, S. G. Nair,
> *Irreducibility of Generalised Laguerre Polynomials for Large Integer Parameters*,
> [arXiv:2610.10614](https://arxiv.org/abs/2610.10614),

together with an extension of its main theorem from a ≤ 1000 to a ≤ 1078.

## Result

For 50 < a ≤ 1078 and n ≥ 2, the generalised Laguerre polynomial L_n^(a)(x) is irreducible
over Q, except when n = 2 and a + 2 is a perfect square (a = m² − 2, 8 ≤ m ≤ 32).

- **50 < a ≤ 1000:** the paper's Theorem 1.1. All its finite computations are re-run here and
  agree with the theorem.
- **1000 < a ≤ 1078:** the same proof, checked to hold unchanged on this range. The only new
  exception is a = 1022. See [EXTENSION.md](EXTENSION.md).

This is not an independent proof. The lemmas that reduce the problem to finite computations,
and several results from the literature, are taken as given.

## Run

Needs [SageMath](https://www.sagemath.org/) (used to factorise polynomials). Then:

```bash
conda env create -f environment.yml && conda activate laguerre
SAGE_PYTHON=python bash run_all.sh
```

This takes about a minute and writes everything to `results/`.

## Read more

- [DOCUMENTATION.md](DOCUMENTATION.md): how the proof works, how to run each step, the
  results and their differences from the paper, the readings of the paper used in the code,
  and what is assumed rather than verified.
- [EXTENSION.md](EXTENSION.md): the extension to a ≤ 1078: where the bound comes from, the
  cases checked, and what blocks going further.
- [REFERENCES.md](REFERENCES.md): the paper, the results it imports, and the software used.
- [results/README.md](results/README.md): what each output file contains.
