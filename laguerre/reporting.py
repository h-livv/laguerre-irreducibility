"""
Logging for the step scripts.

Every step script creates one StepReport and uses it to record three kinds of things:

    log(text)                      a line of free text (survivor counts, explanations)
    checkpoint(name, paper, ours)  a number or list that the paper prints, next to ours
    certificate(n, a, k, record)   the final proof record of one case (see certificates.py)

save() then writes two files into the results/ folder:

    results/<step name>.log    everything that was printed, for humans
    results/<step name>.json   the checkpoints and certificates, read by step09_assemble.py
"""

import json
import os

from laguerre.config import RESULTS_DIRECTORY


def _normalise(value):
    """Convert a value to plain JSON data, so that tuples and lists compare as equal."""
    return json.loads(json.dumps(value, default=str))


class StepReport:
    """Collects the log lines, checkpoints and certificates of one step script."""

    def __init__(self, step_name):
        self.step_name = step_name
        self.lines = []
        self.checkpoints = []
        self.certificates = []
        self.extra = {}

    def log(self, text):
        """Print a line and keep it for the log file."""
        print(text)
        self.lines.append(text)

    def checkpoint(self, description, paper_value, our_value, explanation=""):
        """
        Record a value printed in the paper next to the value we computed.
        Logs MATCH or DIFFERENT. A difference does not stop the script.

        `explanation` is optional text saying why a difference is expected (what we found
        when we investigated it). It is only shown when the two values differ.
        """
        paper_value = _normalise(paper_value)
        our_value = _normalise(our_value)
        matches = paper_value == our_value
        self.checkpoints.append({
            "description": description,
            "paper": paper_value,
            "ours": our_value,
            "matches": matches,
            "explanation": explanation,
        })
        status = "MATCH    " if matches else "DIFFERENT"
        self.log("[checkpoint %s] %s" % (status, description))
        self.log("        paper: %s" % (paper_value,))
        self.log("        ours:  %s" % (our_value,))
        if not matches and explanation != "":
            self.log("        explanation: %s" % explanation)

    def certificate(self, n, a, k, record):
        """Record the certificate that closes the case (n, a, k)."""
        self.certificates.append({"n": n, "a": a, "k": k, "certificate": _normalise(record)})
        self.log("[certificate] (n, a, k) = (%d, %d, %d): %s" % (n, a, k, record))

    def set_extra(self, key, value):
        """Store any other result (for example the list of exceptions) under a name."""
        self.extra[key] = _normalise(value)

    def save(self):
        """Write the .log and .json files of this step into the results/ folder."""
        os.makedirs(RESULTS_DIRECTORY, exist_ok=True)
        log_path = os.path.join(RESULTS_DIRECTORY, self.step_name + ".log")
        with open(log_path, "w") as log_file:
            log_file.write("\n".join(self.lines) + "\n")
        json_path = os.path.join(RESULTS_DIRECTORY, self.step_name + ".json")
        data = {
            "step": self.step_name,
            "checkpoints": self.checkpoints,
            "certificates": self.certificates,
            "extra": self.extra,
        }
        with open(json_path, "w") as json_file:
            json.dump(data, json_file, indent=1)
        print("Saved %s and %s" % (log_path, json_path))
