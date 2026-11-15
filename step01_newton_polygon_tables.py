"""
STEP 1. Reproduce the 8 Newton polygon tables of the paper (Lemmas 5.5 and 5.6).

For each row of the paper's two tables we recompute the Newton polygon and check:

    * the points printed in the paper: every corner (vertex) of our polygon must be in the
      paper's list, and every point of the paper's list must be a lattice point of our
      polygon. (The paper's tables are headed "Vertices" but some rows also list lattice
      points lying on the edges, so we cannot ask for equality with either list.)
    * the slope of the right-most edge;
    * the conclusion: Lemma 2.8 excludes a factor of degree k for this prime.

Run:  $SAGE_PYTHON step01_newton_polygon_tables.py
"""

from fractions import Fraction

from laguerre.newton_polygon import (
    filaseta_excludes_degree,
    lattice_points_on_polygon,
    polygon_summary,
)
from laguerre.reporting import StepReport

# Each row: (n, a, k, p, points printed in the paper, slope of the right-most edge).
PAPER_TABLES = [
    # Table in the proof of Lemma 5.5 (k = 3).
    (25, 527, 3, 29, [(0, 0), (1, 0), (25, 1)], Fraction(1, 24)),
    (56, 845, 3, 17, [(0, 0), (34, 2), (51, 4), (56, 5)], Fraction(1, 5)),
    (65, 167, 3, 29, [(0, 0), (58, 2), (65, 3)], Fraction(1, 7)),
    # Table in the proof of Lemma 5.6 (k = 2).
    (36, 339, 2, 3, [(0, 0), (9, 4), (36, 17)], Fraction(13, 27)),
    (81, 115, 2, 7, [(0, 0), (49, 8), (77, 13), (81, 14)], Fraction(1, 4)),
    (81, 235, 2, 7,
     [(0, 0), (1, 0), (8, 1), (15, 2), (22, 3), (71, 11), (78, 13), (81, 14)], Fraction(1, 3)),
    (81, 544, 2, 3, [(0, 0), (81, 40)], Fraction(40, 81)),
    (81, 648, 2, 7,
     [(0, 0), (1, 0), (8, 1), (15, 2), (22, 3), (29, 4), (78, 13), (81, 14)], Fraction(1, 3)),
]


def main():
    report = StepReport("step01_newton_polygon_tables")

    for (n, a, k, p, paper_points, paper_slope) in PAPER_TABLES:
        summary = polygon_summary(n, a, p)
        vertices = summary["vertices"]
        lattice_points = lattice_points_on_polygon(vertices)
        report.log("")
        report.log("(n, a, k) = (%d, %d, %d), p = %d" % (n, a, k, p))
        report.log("    our vertices:       %s" % (vertices,))
        report.log("    our lattice points: %s" % (lattice_points,))

        vertices_are_listed = all(vertex in paper_points for vertex in vertices)
        paper_points_are_lattice_points = all(point in lattice_points for point in paper_points)
        report.checkpoint(
            "Table row (%d, %d, %d), p = %d: paper's points agree with our polygon" % (n, a, k, p),
            True,
            vertices_are_listed and paper_points_are_lattice_points,
        )
        report.checkpoint(
            "Table row (%d, %d, %d), p = %d: slope of the right-most edge" % (n, a, k, p),
            str(paper_slope),
            str(summary["slopes"][0]),
        )
        report.checkpoint(
            "Table row (%d, %d, %d), p = %d: Lemma 2.8 excludes degree k" % (n, a, k, p),
            True,
            filaseta_excludes_degree(n, a, k, p),
        )

    report.save()


if __name__ == "__main__":
    main()
