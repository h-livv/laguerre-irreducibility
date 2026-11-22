# results/

This folder is filled by the scripts. Re-running a script overwrites its files.

- **50 < a ≤ 1000** (the paper's range): the files in this folder, from the run of 2026-11-14.
  Start with `summary.md`.
- **1000 < a ≤ 1078** (the extension): the folder `extension_a1078/`, from the run of
  2026-11-21. Start with `extension_a1078/summary.md`; the conclusions are in
  [`../EXTENSION.md`](../EXTENSION.md).

| File | Written by | Content |
| --- | --- | --- |
| `stepNN_*.log` | each step script | everything the step printed: counts, checkpoints, certificates |
| `stepNN_*.json` | each step script | the same checkpoints and certificates as data |
| `summary.md` | `step09_assemble.py` | verdict, checkpoint table (paper vs ours), certificate counts, imports |
| `deliverable.html` | `step11_deliverable_page.py` | the one-page deliverable: theorem, funnels, certificates with Newton polygons, imports, differences |
| `extension_a1078/summary.md` | `extension_a1078.py` | verdict, audit of the bound on a, certificate counts for 1000 < a ≤ 1078 |
| `extension_a1078/audit.json` | `extension_a1078.py` | the audit as data: each statement and the largest a it allows |
| `extension_a1078/stepNN_*.log`, `.json` | `extension_a1078.py` | steps 2, 6, 7, 8 on 1000 < a ≤ 1078; checkpoints are logged as plain counts |
