#!/usr/bin/env bash
# Run the whole reproduction, step by step, from the repository root.
#
# Usage:
#     bash run_all.sh                                        # Sage installed the classic way
#     SAGE_PYTHON=python bash run_all.sh                     # inside an activated conda/mamba Sage environment
#
# SAGE_PYTHON is the Python interpreter that can "import sage". It defaults to "sage -python".
# A conda/mamba installation of Sage has no "-python" option; there, point SAGE_PYTHON at the
# "python" inside the Sage environment (see README.md, "How to run").
#
# Each step writes results/<step>.log and results/<step>.json; step 9 writes results/summary.md.

set -e                      # stop at the first step that crashes
cd "$(dirname "$0")"        # always run from the repository root

SAGE_PYTHON="${SAGE_PYTHON:-sage -python}"

$SAGE_PYTHON step01_newton_polygon_tables.py
$SAGE_PYTHON step02_small_n_and_baseline.py
$SAGE_PYTHON step03_lemma_2_6.py
$SAGE_PYTHON step04_stormer_data.py
$SAGE_PYTHON step05_k_at_least_6.py
$SAGE_PYTHON step06_k345_lemma_5_5.py
$SAGE_PYTHON step07_k2_lemma_5_6.py
$SAGE_PYTHON step08_k1_lemmas_6_5_6_6.py
$SAGE_PYTHON step09_assemble.py

# Step 10: the property tests.
$SAGE_PYTHON tests/test_properties.py

# Step 11: the one-page deliverable, results/deliverable.html.
$SAGE_PYTHON step11_deliverable_page.py
