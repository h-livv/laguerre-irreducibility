"""
Newton polygons of the Laguerre polynomial.

The polynomial. We work with the scaled polynomial (Section 1 of the paper)

    script-L_n^(a)(x) = n! L_n^(a)(x) = sum_{j=0}^{n} (-1)^j a_j x^j,
    a_j = C(n, j) (n+a)! / (j+a)!,

which is monic up to sign and has integer coefficients. In this file `a` is always the
parameter of the polynomial and `a_j` is always a coefficient.

ORIENTATION (Section 2.1). The Newton polygon with respect to a prime p is the lower convex
hull of the points

    (n - j, nu_p(a_j))   for j = n, n-1, ..., 0.

So x = 0 is the leading coefficient a_n = 1 and x = n is the constant coefficient a_0.
The RIGHT-MOST edge therefore comes from the low-degree coefficients (small j).
Signs do not matter: only |a_j| enters.

Valuations are computed with Legendre's formula; the huge numbers a_j are never built here.
"""

from fractions import Fraction
from math import gcd

from laguerre.arithmetic import (
    binomial_valuation,
    delta_valuation,
    factorial_valuation,
    subset_sums,
)


# ----------------------------------------------------------------------------------------
# Valuations of the coefficients.
# ----------------------------------------------------------------------------------------

def coefficient_valuation(n, a, j, p):
    """
    nu_p(a_j) for a_j = C(n, j) (n+a)! / (j+a)!, by Legendre's formula:

        nu_p(a_j) = nu_p(C(n, j)) + nu_p((n+a)!) - nu_p((j+a)!).
    """
    return (
        binomial_valuation(n, j, p)
        + factorial_valuation(n + a, p)
        - factorial_valuation(j + a, p)
    )


def phi(n, a, j, p):
    """
    phi_j(p) of equation (4): the slope of the segment joining the point of a_j, which is
    (n - j, nu_p(a_j)), to the right end point (n, nu_p(a_0)). Returned as an exact Fraction.

        phi_j(p) = ( nu_p(Delta(a+1, j)) - nu_p(C(n, j)) ) / j,     1 <= j <= n.

    By equation (5) the slope of the right-most edge is the maximum of phi_j(p) over j.
    """
    numerator = delta_valuation(a + 1, j, p) - binomial_valuation(n, j, p)
    return Fraction(numerator, j)


# ----------------------------------------------------------------------------------------
# The Newton polygon.
# ----------------------------------------------------------------------------------------

def newton_polygon_points(n, a, p):
    """Return the n + 1 points (x, nu_p(a_{n-x})) for x = 0, 1, ..., n."""
    points = []
    for x in range(0, n + 1):
        j = n - x
        points.append((x, coefficient_valuation(n, a, j, p)))
    return points


def lower_convex_hull(points):
    """
    Return the vertices of the lower convex hull of `points`, from left to right.

    The points must be sorted by x, with distinct x. Points that lie ON an edge but are not
    corners are NOT returned (see lattice_points_on_polygon for those). Only integer
    arithmetic is used (a cross product decides each turn).
    """
    hull = []
    for point in points:
        while len(hull) >= 2:
            (x1, y1) = hull[-2]
            (x2, y2) = hull[-1]
            (x3, y3) = point
            cross_product = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
            # cross_product <= 0 means the middle point is on or above the line from the
            # first to the third point, so it is not a corner of the lower hull.
            if cross_product <= 0:
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


def newton_polygon_vertices(n, a, p):
    """Return the vertices (corners) of the Newton polygon NP_p, from left to right."""
    return lower_convex_hull(newton_polygon_points(n, a, p))


def lattice_points_on_polygon(vertices):
    """
    Return every point with integer coordinates lying on the polygon with the given
    vertices, from left to right. This includes the vertices themselves.

    The paper's tables sometimes list these lattice points and sometimes only the vertices.
    """
    lattice_points = [vertices[0]]
    for index in range(1, len(vertices)):
        (x1, y1) = vertices[index - 1]
        (x2, y2) = vertices[index]
        width = x2 - x1
        height = y2 - y1
        number_of_segments = gcd(width, height)
        for step in range(1, number_of_segments + 1):
            x = x1 + step * (width // number_of_segments)
            y = y1 + step * (height // number_of_segments)
            lattice_points.append((x, y))
    return lattice_points


def polygon_summary(n, a, p):
    """
    Return the Newton polygon NP_p in the notation of the paper, as a dictionary:

        "vertices"  the corners, from left to right
        "slopes"    slopes[i-1] = phi^(i), the slope of the i-th edge counted FROM THE RIGHT
        "r"         r[i-1] = r_i, where n - r_i is the x-coordinate of the i-th vertex from the
                    right (not counting the end point x = n). So r_1 is the horizontal
                    length of the right-most edge, and the last r_i equals n.
    """
    vertices = newton_polygon_vertices(n, a, p)
    slopes = []
    r = []
    for index in range(len(vertices) - 1, 0, -1):
        (x_left, y_left) = vertices[index - 1]
        (x_right, y_right) = vertices[index]
        slopes.append(Fraction(y_right - y_left, x_right - x_left))
        r.append(n - x_left)
    return {"vertices": vertices, "slopes": slopes, "r": r}


def rightmost_slope(n, a, p):
    """phi^(1): the slope of the right-most edge of NP_p, as an exact Fraction."""
    return polygon_summary(n, a, p)["slopes"][0]


# ----------------------------------------------------------------------------------------
# Dumas degree sets (Lemma 2.7).
# ----------------------------------------------------------------------------------------

def dumas_degree_set(n, a, p):
    """
    Return D_p(n, a): the set of degrees that a factor is allowed to have by Dumas' theorem.

    The lattice points cut the polygon into segments. An edge of width w whose slope in
    lowest terms has denominator s is cut into w / s segments of width s. By Lemma 2.7 the
    degree of any factor in Z[x] is a sum of some of these segment widths.

    So: if k is NOT in D_p(n, a) for some prime p, there is no factor of degree k.
    """
    vertices = newton_polygon_vertices(n, a, p)
    segment_widths = []
    for index in range(1, len(vertices)):
        (x1, y1) = vertices[index - 1]
        (x2, y2) = vertices[index]
        width = x2 - x1
        height = y2 - y1
        number_of_segments = gcd(width, height)
        for _ in range(number_of_segments):
            segment_widths.append(width // number_of_segments)
    return subset_sums(segment_widths)


# ----------------------------------------------------------------------------------------
# The Filaseta check (Lemma 2.8 combined with Lemma 2.9(ii)).
# ----------------------------------------------------------------------------------------

def prime_divides_filaseta_product(n, a, k, p):
    """
    Return True if p divides Delta(n-k+1, k) * Delta(n+a-k+1, k).

    By Lemma 2.9(ii) this guarantees p does not divide a_n and p | a_j for 0 <= j <= n-k,
    which are the hypotheses of Lemma 2.8.
    """
    for i in range(0, k):
        if (n - i) % p == 0:
            return True
        if (n + a - i) % p == 0:
            return True
    return False


def filaseta_excludes_degree(n, a, k, p):
    """
    Return True if Lemma 2.8 with the prime p proves that there is NO factor of degree k.

    The conditions are: p | Delta(n-k+1, k) * Delta(n+a-k+1, k), and the right-most edge of
    NP_p has slope < 1/k.
    """
    if not prime_divides_filaseta_product(n, a, k, p):
        return False
    return rightmost_slope(n, a, p) < Fraction(1, k)
