# results/

This folder is filled by the step scripts. The files here are from the run of 2026-11-14.
Start with `summary.md`. Re-running a step overwrites its files.

| File | Written by | Content |
| --- | --- | --- |
| `stepNN_*.log` | each step script | everything the step printed: counts, checkpoints, certificates |
| `stepNN_*.json` | each step script | the same checkpoints and certificates as data |
| `summary.md` | `step09_assemble.py` | verdict, checkpoint table (paper vs ours), certificate counts, imports |
| `deliverable.html` | `step11_deliverable_page.py` | the one-page deliverable: theorem, funnels, certificates with Newton polygons, imports, differences |
