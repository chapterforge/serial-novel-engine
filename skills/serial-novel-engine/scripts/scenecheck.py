# -*- coding: utf-8 -*-
"""Scene-vs-essay gate. Catches the failure a word count cannot see.

A first-person narrator will quietly stop dramatising and start summarising,
because summary is easier and sounds like voice. Readers feel it as "nothing
happens". This measures it.

    python scenecheck.py                      # whole manuscript, failures only
    python scenecheck.py ch_041-044.txt       # one file, full table
    python scenecheck.py --dir path/to/manuscript

Rules:
  1. A chapter with <20% dialogue paragraphs is an ESSAY.
  2. Never two essays in a row.
  3. At most one essay in any four consecutive chapters.

Essays are allowed. They are a seasoning, not a diet.
"""
import argparse, glob, io, os, re, sys

ESSAY_PC = 20


def chapters(files):
    out = []
    for f in files:
        s = io.open(f, encoding="utf-8").read()
        parts = re.split(r"===CHAPTER (\d+)===", s)
        for i in range(1, len(parts), 2):
            n = int(parts[i])
            paras = [p for p in parts[i + 1].split("\n\n") if p.strip()]
            dlg = sum(1 for p in paras if p.lstrip().startswith(('"', "“")))
            pc = round(100 * dlg / max(1, len(paras)))
            out.append((n, len(paras), dlg, pc))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--dir", default="manuscript")
    a = ap.parse_args()

    if a.files:
        files = [f if os.path.exists(f) else os.path.join(a.dir, f) for f in a.files]
        verbose = True
    else:
        files = sorted(glob.glob(os.path.join(a.dir, "ch_*.txt")))
        verbose = False
    if not files:
        sys.exit("No ch_*.txt files found in %r. Pass --dir." % a.dir)

    rows = chapters(files)
    fails = []
    for idx, (n, p, d, pc) in enumerate(rows):
        essay = pc < ESSAY_PC
        if verbose:
            print("  Ch %-4d %3d paras %3d dialogue %4d%%  %s"
                  % (n, p, d, pc, "ESSAY" if essay else "scene"))
        if not essay:
            continue
        prev_essay = idx > 0 and rows[idx - 1][3] < ESSAY_PC
        if prev_essay:
            fails.append("Ch %d and %d are BOTH essays (rule 2: never consecutive)"
                         % (rows[idx - 1][0], n))
        win = [r for r in rows[max(0, idx - 3):idx + 1] if r[3] < ESSAY_PC]
        if len(win) > 1 and not prev_essay:
            fails.append("Ch %d: %d essays inside Ch %d-%d (rule 3: max 1 in 4)"
                         % (n, len(win), rows[max(0, idx - 3)][0], n))

    print()
    if fails:
        print("  SCENE GATE: %d FAILURES" % len(fails))
        for f in fails:
            print("   -", f)
        sys.exit(1)
    print("  SCENE GATE: CLEAN")


if __name__ == "__main__":
    main()
