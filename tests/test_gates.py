# -*- coding: utf-8 -*-
"""Prove every gate can fail, and can pass.

    python tests/test_gates.py

A check that has never been seen failing can't be trusted: in a real pipeline, two checks once
searched for a backspace byte (a regex \\b mangled by a shell heredoc) for two whole books and never
fired. So each gate runs on a manuscript that must pass and one that must fail, and the scripts are
scanned for that byte. Standard library only; exit 0 when every expectation holds. CI runs this.
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "serial-novel-engine", "scripts")
GOOD = os.path.join(ROOT, "examples", "manuscript")
BAD = os.path.join(ROOT, "examples", "broken")
SMALL_BAND = ["--lo", "50", "--hi", "300", "--ch1-lo", "50", "--ch1-hi", "300"]  # the example chapters are short

CASES = [
    # (label, script, args, expected exit code, text that must appear)
    ("wc passes a manuscript in band", "wc.py", ["--dir", GOOD, "ch_001-002.txt"] + SMALL_BAND, 0, "All in band"),
    ("wc fails chapters under the band", "wc.py", ["--dir", BAD, "ch_003-006.txt"], 1, "SHORT"),
    ("scenecheck passes a single essay", "scenecheck.py", ["--dir", GOOD], 0, "SCENE GATE: CLEAN"),
    ("scenecheck fails two essays in a row", "scenecheck.py", ["--dir", BAD], 1, "BOTH essays"),
    ("cliche_check passes clean prose", "cliche_check.py", ["--dir", GOOD], 0, "VERDICT: CLEAN"),
    ("cliche_check fails em-dashes and stock phrases", "cliche_check.py", ["--dir", BAD], 1, "NEEDS WORK"),
]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    failed = 0
    for label, script, args, want_rc, needle in CASES:
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + args, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (r.stderr or "")
        ok = r.returncode == want_rc and needle in out
        failed += not ok
        print("  %s  %s" % ("ok  " if ok else "FAIL", label))
        if not ok:
            print("        expected exit %d with %r, got exit %d" % (want_rc, needle, r.returncode))
            for line in out.strip().splitlines()[-8:]:
                print("        | " + line)
    bad = [f for f in sorted(os.listdir(SCRIPTS)) if f.endswith(".py")
           and b"\x08" in open(os.path.join(SCRIPTS, f), "rb").read()]
    failed += bool(bad)
    print("  %s  no backspace bytes in any script%s" % ("ok  " if not bad else "FAIL", (": " + ", ".join(bad)) if bad else ""))
    total = len(CASES) + 1
    print("\n%d checks, %d failed." % (total, failed))
    print("GATES: %s" % ("ALL PROVEN" if not failed else "FAILURES"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
