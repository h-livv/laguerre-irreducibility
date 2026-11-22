"""
STEP 11. Build a one-page overview of the results: results/deliverable.html.

This script computes nothing new about the theorem. It reads the results/*.json files of
steps 2, 6, 7 and 8 and lays them out as one HTML page with four parts:

    1. the theorem and its exceptions;
    2. one elimination funnel per branch (k = 3-5, k = 2, k = 1): the paper's counts next to ours;
    3. the certificates of the final cases, with each Newton polygon drawn;
    4. the imports, and the differences from the paper that are still open.

The only computation here is re-drawing the Newton polygons of the final cases (the eight
of the paper's tables and the two extra cases we found for n = 81).

The output is an HTML fragment (no <html> or <body> tags), which is the format expected
when the page is published as an artifact. It can also be opened directly in a browser.

Run:  $SAGE_PYTHON step11_deliverable_page.py      (plain python3 also works for this step)
"""

import html
import json
import os

from laguerre.config import A_MAX, A_MIN, RESULTS_DIRECTORY
from laguerre.newton_polygon import newton_polygon_points, polygon_summary

# The final cases closed by a Newton polygon: (n, a, k, p, where it comes from).
POLYGON_CASES = [
    (25, 527, 3, 29, "paper, Lemma 5.5"),
    (56, 845, 3, 17, "paper, Lemma 5.5"),
    (65, 167, 3, 29, "paper, Lemma 5.5"),
    (36, 339, 2, 3, "paper, Lemma 5.6"),
    (81, 115, 2, 7, "paper, Lemma 5.6"),
    (81, 235, 2, 7, "paper, Lemma 5.6"),
    (81, 544, 2, 3, "paper, Lemma 5.6"),
    (81, 648, 2, 7, "paper, Lemma 5.6"),
    (81, 144, 2, 3, "extra case, not in the paper's list"),
    (81, 360, 2, 3, "extra case, not in the paper's list"),
]

BRANCHES = [
    ("step06_k345_lemma_5_5", "Degree 3, 4, 5", "Lemma 5.5"),
    ("step07_k2_lemma_5_6", "Degree 2", "Lemma 5.6"),
    ("step08_k1_lemmas_6_5_6_6", "Degree 1, n ≥ 4", "Lemmas 6.5 and 6.6"),
]

IMPORTS = [
    "Lemmas 2.1, 2.2, 2.3 and 2.10 (Laishram–Shorey, Nair–Shorey, Najman), and the deduction of "
    "Lemma 5.2 from them: no factor of degree k ≥ 6.",
    "Lehmer's Tables IA and IB: no m > 1,611,308,700 has P(m(m−1)) ≤ 31. Our enumeration agrees up to 10¹⁰.",
    "Szegő's bounds on the zeros of Laguerre polynomials (Lemma 6.4).",
    "The whole range 0 ≤ a ≤ 50 (Laishram–Shorey). Its 8 exceptions were spot-checked.",
    "The proofs of the filter lemmas 4.1–4.3, 5.1, 5.3, 5.4, 6.1–6.3 and of Proposition 1.3.",
]

# Findings that are not checkpoint differences (see DOCUMENTATION.md, "Results").
OTHER_FINDINGS = [
    ("Lemma 6.6, the count 366",
     "Reproduced exactly only when the p = 3 condition of Lemma 5.4(ii) is left out. With it, 296 pairs "
     "remain, and (768, 480) from the paper's list of 11 large pairs drops out."),
    ("Lemma 6.1(iii), statement against proof",
     "The statement and the proof differ in two places. The paper's own list contains (576, 482), which "
     "the literal statement would remove, so the proof's version is the one consistent with that list."),
    ("Lemma 4.3, “r₂ ≠ p”",
     "The proof only excludes “r₂ = p and φ⁽²⁾ ≥ 1/k”. On the polygon alone r₂ = p does occur: "
     "(n, a, k, p) = (352, 845, 2, 11) has r₁ = 2, r₂ = 11, φ⁽²⁾ = 1/9. Nothing downstream needs it."),
]


def load_step(step_name):
    """Read results/<step_name>.json."""
    with open(os.path.join(RESULTS_DIRECTORY, step_name + ".json")) as json_file:
        return json.load(json_file)


def short(value):
    """Show a checkpoint value compactly: long lists are replaced by their length."""
    if isinstance(value, list) and len(value) > 4:
        return "%d items" % len(value)
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return html.escape(json.dumps(value).replace('"', ""))


def status_chip(checkpoint):
    """Return the HTML of the small status label of one checkpoint."""
    if checkpoint["matches"]:
        return '<span class="chip ok">match</span>'
    if checkpoint.get("explanation", "").startswith("UNEXPLAINED"):
        return '<span class="chip open">differs, open</span>'
    return '<span class="chip warn">differs, explained</span>'


def funnel_table(step):
    """Return the HTML table of all checkpoints of one step: stage, paper, ours, status."""
    rows = []
    for checkpoint in step["checkpoints"]:
        rows.append(
            "<tr><td>%s</td><td class='num'>%s</td><td class='num'>%s</td><td>%s</td></tr>"
            % (html.escape(checkpoint["description"]), short(checkpoint["paper"]),
               short(checkpoint["ours"]), status_chip(checkpoint))
        )
    return (
        "<div class='scroll'><table><thead><tr><th>Stage</th><th class='num'>Paper</th>"
        "<th class='num'>Ours</th><th>Status</th></tr></thead><tbody>%s</tbody></table></div>"
        % "".join(rows)
    )


def certificate_counts(step):
    """Return a dictionary: certificate type -> number of cases, for one step."""
    counts = {}
    for certificate in step["certificates"]:
        certificate_type = certificate["certificate"]["type"]
        counts[certificate_type] = counts.get(certificate_type, 0) + 1
    return counts


def polygon_svg(n, a, p):
    """
    Draw the Newton polygon NP_p of script-L_n^(a) as an SVG picture.
    Dots are the points (x, nu_p(a_{n-x})); the line is the polygon; the thick last
    segment is the right-most edge, whose slope decides Lemma 2.8.
    """
    width, height = 280, 150
    left, right, top, bottom = 30, 12, 12, 24
    vertices = polygon_summary(n, a, p)["vertices"]
    y_max = max(1, vertices[-1][1])

    def sx(x):
        return left + x * (width - left - right) / n

    def sy(y):
        return height - bottom - y * (height - top - bottom) / y_max

    parts = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Newton polygon for n = %d, a = %d, p = %d">'
             % (width, height, n, a, p)]
    # Axes.
    parts.append('<line class="axis" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (sx(0), sy(0), sx(n), sy(0)))
    parts.append('<line class="axis" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (sx(0), sy(0), sx(0), sy(y_max)))
    # The points of all coefficients (those above the frame are not shown).
    for (x, y) in newton_polygon_points(n, a, p):
        if y <= y_max:
            parts.append('<circle class="dot" cx="%.1f" cy="%.1f" r="1.3"/>' % (sx(x), sy(y)))
    # The polygon, then its right-most edge once more, thicker.
    path = " ".join("%.1f,%.1f" % (sx(x), sy(y)) for (x, y) in vertices)
    parts.append('<polyline class="hull" points="%s"/>' % path)
    (x1, y1), (x2, y2) = vertices[-2], vertices[-1]
    parts.append('<line class="edge" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (sx(x1), sy(y1), sx(x2), sy(y2)))
    for (x, y) in vertices:
        parts.append('<circle class="vertex" cx="%.1f" cy="%.1f" r="2.6"/>' % (sx(x), sy(y)))
    # Axis labels: 0 and n on the x-axis, the largest valuation on the y-axis.
    parts.append('<text class="lbl" x="%.1f" y="%d" text-anchor="middle">0</text>' % (sx(0), height - 8))
    parts.append('<text class="lbl" x="%.1f" y="%d" text-anchor="end">x = %d</text>' % (sx(n), height - 8, n))
    parts.append('<text class="lbl" x="%.1f" y="%.1f" text-anchor="end">%d</text>' % (left - 5, sy(y_max) + 4, y_max))
    parts.append("</svg>")
    return "".join(parts)


def polygon_cards():
    """Return the HTML of one card per final case closed by a Newton polygon."""
    cards = []
    for (n, a, k, p, source) in POLYGON_CASES:
        summary = polygon_summary(n, a, p)
        slope = summary["slopes"][0]
        vertices_text = ", ".join("(%d, %d)" % (x, y) for (x, y) in summary["vertices"])
        extra_class = " extra" if source.startswith("extra") else ""
        cards.append(
            "<figure class='poly%s'>%s<figcaption>"
            "<strong>(n, a) = (%d, %d)</strong>, k = %d, p = %d<br>"
            "right-most slope <span class='num'>%s</span> &lt; 1/%d<br>"
            "<span class='muted'>vertices %s</span><br><span class='muted'>%s</span>"
            "</figcaption></figure>"
            % (extra_class, polygon_svg(n, a, p), n, a, k, p, slope, k, vertices_text, html.escape(source))
        )
    return "<div class='polys'>%s</div>" % "".join(cards)


def root_search_table(step):
    """Return the HTML table of the cases closed by an integer-root search."""
    rows = []
    for certificate in step["certificates"]:
        record = certificate["certificate"]
        if record["type"] != "root_search":
            continue
        rows.append(
            "<tr><td class='num'>%d</td><td class='num'>%d</td><td class='num'>%d</td><td class='num'>%d</td>"
            "<td class='num'>%d</td><td class='num'>%s</td><td class='num'>%d</td></tr>"
            % (certificate["n"], certificate["a"], record["szego_bound"],
               record["radical_of_n_times_n_plus_a"], record["number_of_direct_candidates"],
               short(record["proposition_1_3_candidates"]), len(record["roots_found"]))
        )
    return (
        "<div class='scroll'><table><thead><tr><th class='num'>n</th><th class='num'>a</th>"
        "<th class='num'>Bound B on ξ</th><th class='num'>Rad(n(n+a))</th><th class='num'>ξ tested</th>"
        "<th class='num'>ξ left by Prop. 1.3</th><th class='num'>Roots</th></tr></thead>"
        "<tbody>%s</tbody></table></div>" % "".join(rows)
    )


PAGE_STYLE = """
<title>Laguerre Irreducibility Reproduction</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* Layout: one reading column; wide tables and the polygon grid scroll or wrap inside it. */
:root {
  --bg: #f7f8fa; --surface: #ffffff; --fg: #1a2230; --muted: #5b6676; --line: #dde2ea;
  --accent: #2456a6; --ok: #1f7a4d; --ok-bg: #e3f3ea; --warn: #8a5a00; --warn-bg: #fbefd2;
  --open: #9b2c2c; --open-bg: #fbe4e4;
  --display: "Space Grotesk", "Inter", system-ui, sans-serif;
  --body: "Inter", system-ui, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #12161d; --surface: #1a2029; --fg: #e6eaf0; --muted: #9aa5b5; --line: #2c3542;
  --accent: #7fb0f5; --ok: #6fd3a0; --ok-bg: #173527; --warn: #f0c060; --warn-bg: #3a2f12;
  --open: #f59a9a; --open-bg: #3d1c1c; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #12161d; --surface: #1a2029; --fg: #e6eaf0; --muted: #9aa5b5; --line: #2c3542;
  --accent: #7fb0f5; --ok: #6fd3a0; --ok-bg: #173527; --warn: #f0c060; --warn-bg: #3a2f12;
  --open: #f59a9a; --open-bg: #3d1c1c; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 15px; line-height: 1.55; }
main { max-width: 960px; margin: 0 auto; padding-block: 32px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 20px; }
h1, h2, h3 { font-family: var(--display); text-wrap: balance; margin: 0; line-height: 1.2; }
h1 { font-size: 30px; } h2 { font-size: 21px; margin-top: 20px; } h3 { font-size: 16px; margin-top: 8px; }
p { margin: 0; max-width: 68ch; }
.muted { color: var(--muted); } .num { font-family: var(--mono); font-variant-numeric: tabular-nums; font-size: 13px; }
.statement { background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--accent);
  padding: 16px 18px; display: flex; flex-direction: column; gap: 10px; }
.facts { display: flex; flex-wrap: wrap; gap: 8px 28px; }
.facts div { display: flex; flex-direction: column; }
.facts b { font-family: var(--display); font-size: 22px; }
.exceptions { display: flex; flex-wrap: wrap; gap: 6px; }
.exceptions span { font-family: var(--mono); font-size: 12.5px; border: 1px solid var(--line); background: var(--surface); padding: 2px 7px; }
.scroll { overflow-x: auto; min-width: 0; }
table { border-collapse: collapse; width: 100%; font-size: 13.5px; }
th, td { text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-weight: 600; color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }
th.num, td.num { text-align: right; white-space: nowrap; }
.chip { font-size: 12px; padding: 1px 8px; border-radius: 10px; white-space: nowrap; }
.chip.ok { color: var(--ok); background: var(--ok-bg); } .chip.warn { color: var(--warn); background: var(--warn-bg); }
.chip.open { color: var(--open); background: var(--open-bg); }
.polys { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; }
figure.poly { margin: 0; background: var(--surface); border: 1px solid var(--line); padding: 10px; min-width: 0; }
figure.poly.extra { border-color: var(--warn); }
figure.poly svg { width: 100%; height: auto; display: block; }
figcaption { font-size: 12.5px; line-height: 1.5; margin-top: 6px; overflow-wrap: anywhere; }
.axis { stroke: var(--line); stroke-width: 1; } .dot { fill: var(--muted); opacity: 0.45; }
.hull { fill: none; stroke: var(--fg); stroke-width: 1.2; } .edge { stroke: var(--accent); stroke-width: 3; }
.vertex { fill: var(--surface); stroke: var(--fg); stroke-width: 1.2; } .lbl { fill: var(--muted); font-family: var(--mono); font-size: 9px; }
ul { margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px; max-width: 72ch; }
.diff { display: flex; flex-direction: column; gap: 10px; }
.diff div { background: var(--surface); border: 1px solid var(--line); padding: 10px 14px; }
.diff b { display: block; }
</style>
"""


def main():
    step02 = load_step("step02_small_n_and_baseline")
    steps = {name: load_step(name) for (name, title, lemma) in BRANCHES}

    all_checkpoints = []
    for step_name in sorted(os.listdir(RESULTS_DIRECTORY)):
        if step_name.endswith(".json"):
            all_checkpoints.extend(load_step(step_name[:-5])["checkpoints"])
    number_matching = len([c for c in all_checkpoints if c["matches"]])
    number_of_certificates = len(step02["certificates"]) + sum(len(s["certificates"]) for s in steps.values())

    parts = [PAGE_STYLE, "<main>"]

    # ------------------------------------------------------------- 1. theorem and exceptions
    parts.append("<header><p class='muted'>A personal, unofficial reproduction of the computations in "
                 "Das–Dutta–Laishram–Nair, arXiv:2610.10614</p>"
                 "<h1>Laguerre irreducibility for %d &lt; a ≤ %d</h1></header>" % (A_MIN, A_MAX))
    exceptions = step02["extra"]["exceptions"]
    parts.append(
        "<section class='statement'><p><strong>The computations agree with Theorem 1.1 of the paper.</strong> "
        "The theorem: for %d &lt; a ≤ %d and n ≥ 2, L<sub>n</sub><sup>(a)</sup>(x) is irreducible over Q, "
        "except when n = 2 and a + 2 is a perfect square, where it has a linear factor.</p>"
        "<p class='muted'>This is a re-run of the finite computations of the paper's proof, not an independent "
        "proof. The lemmas that reduce the problem to these computations, and the results listed under "
        "“Imports”, are taken as given. It has not been reviewed by the paper's authors.</p>"
        "<div class='facts'><div><b>%d</b><span class='muted'>exceptions, all n = 2</span></div>"
        "<div><b>%d</b><span class='muted'>cases closed by a certificate</span></div>"
        "<div><b>0</b><span class='muted'>cases left open</span></div>"
        "<div><b>%d of %d</b><span class='muted'>checkpoints equal the paper</span></div></div></section>"
        % (A_MIN, A_MAX, len(exceptions), number_of_certificates, number_matching, len(all_checkpoints))
    )
    parts.append("<h3>The exceptions: n = 2, a = m² − 2 for 8 ≤ m ≤ 31</h3><div class='exceptions'>%s</div>"
                 % "".join("<span>%d</span>" % a for (n, a) in exceptions))

    # ------------------------------------------------------------- 2. funnels
    parts.append("<h2>Elimination funnels: the paper's counts next to ours</h2>"
                 "<p>Each row is a number or a list that the paper prints while narrowing “all n” down to a "
                 "finite set. Lists longer than four entries are shown by their length.</p>")
    for (step_name, title, lemma) in BRANCHES:
        counts = certificate_counts(steps[step_name])
        counts_text = ", ".join("%d by %s" % (counts[key], key.replace("_", " ")) for key in sorted(counts))
        parts.append("<h3>%s <span class='muted'>(%s)</span></h3>" % (title, lemma))
        parts.append(funnel_table(steps[step_name]))
        parts.append("<p class='muted'>Cases left after the filters, all closed: %s.</p>" % counts_text)
    parts.append("<p class='muted'>Degree ≥ 6 is covered by the imported Lemma 5.2; n = 2 and n = 3 by "
                 "Theorem 1.2, checked by factorisation.</p>")

    # ------------------------------------------------------------- 3. certificates
    parts.append("<h2>Certificates of the final cases</h2>"
                 "<h3>Closed by a Newton polygon (Lemma 2.8)</h3>"
                 "<p>The thick segment is the right-most edge. Its slope is below 1/k, so there is no factor of "
                 "degree k. Dots are the valuations of all coefficients. The two outlined cards are cases that "
                 "survive the filters as read here but are not in the paper's list.</p>")
    parts.append(polygon_cards())
    parts.append("<h3>Closed by an integer-root search (degree 1, n &gt; 300)</h3>"
                 "<p>Every multiple of Rad(n(n+a)) up to Szegő's bound B was tested. None is a root.</p>")
    parts.append(root_search_table(steps["step08_k1_lemmas_6_5_6_6"]))
    parts.append("<p class='muted'>All other final cases were closed by full factorisation over Q, or (44 small "
                 "cases of degree 2) by a Newton polygon. The individual records are in the results/*.json files.</p>")

    # ------------------------------------------------------------- 4. imports and differences
    parts.append("<h2>Imports: assumed, not verified here</h2><ul>%s</ul>"
                 % "".join("<li>%s</li>" % text for text in IMPORTS))
    parts.append("<h2>Differences from the paper</h2>"
                 "<p>None affects the theorem: every case that survives the filters here is closed by a certificate. "
                 "A difference may come from a step the paper does not spell out, or from a misreading on my side.</p>")
    difference_cards = []
    for checkpoint in all_checkpoints:
        if not checkpoint["matches"]:
            difference_cards.append("<div><b>%s %s</b>Paper: <span class='num'>%s</span> · ours: "
                                    "<span class='num'>%s</span><br>%s</div>"
                                    % (html.escape(checkpoint["description"]), status_chip(checkpoint),
                                       short(checkpoint["paper"]), short(checkpoint["ours"]),
                                       html.escape(checkpoint.get("explanation", ""))))
    parts.append("<div class='diff'>%s</div>" % "".join(difference_cards))
    parts.append("<h3>Other findings</h3><div class='diff'>%s</div>"
                 % "".join("<div><b>%s</b>%s</div>" % (title, text) for (title, text) in OTHER_FINDINGS))

    parts.append("</main>")

    output_path = os.path.join(RESULTS_DIRECTORY, "deliverable.html")
    with open(output_path, "w") as output_file:
        output_file.write("\n".join(parts))
    print("Saved %s" % output_path)


if __name__ == "__main__":
    main()
