"""
Library code for reproducing Das-Dutta-Laishram-Nair (arXiv 2610.10614):
irreducibility of the generalised Laguerre polynomials L_n^(a)(x) for 50 < a <= 1000.

Modules (read them in this order):

    config.py          constants: the range of a, file locations, limits
    arithmetic.py      integer helpers: valuations, P(m), Rad(m), Delta(m, l), Section 4 quantities
    newton_polygon.py  Newton polygons of the Laguerre polynomial, Dumas degree sets, Filaseta check
    oracles.py         exact checks on one polynomial: factorisation, integer-root search
    stormer.py         smooth numbers and Stormer numbers (Lehmer's Table IA, recomputed)
    filters.py         one function per lemma of the paper that eliminates cases (n, a, k)
    certificates.py    builds the final proof record ("certificate") for one case (n, a, k)
    reporting.py       logging of counts, checkpoints and certificates to the results/ folder
"""
