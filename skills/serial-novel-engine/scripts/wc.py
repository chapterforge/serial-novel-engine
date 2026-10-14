# -*- coding: utf-8 -*-
"""Per-chapter word count with the gap to the band.

    python wc.py                          # newest ch_*.txt in ./manuscript
    python wc.py ch_041-044.txt           # one or more files
    python wc.py --dir path/to/manuscript ch_041-044.txt
    python wc.py --lo 1500 --hi 1800      # different band

Counts the chapter body (title line dropped) by whitespace split. Shows the
shortfall so one corrective pass can be sized to close it.
"""
import argparse, io, os, re, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--dir", default="manuscript")
    ap.add_argument("--lo", type=int, default=1000)
    ap.add_argument("--hi", type=int, default=1150)
    ap.add_argument("--ch1-lo", type=int, default=1800)
    ap.add_argument("--ch1-hi", type=int, default=2200)
    a = ap.parse_args()

    files = a.files
    if not files:
        if not os.path.isdir(a.dir):
            sys.exit("No manuscript folder at %r. Pass --dir." % a.dir)
        files = sorted(f for f in os.listdir(a.dir) if f.startswith("ch_"))[-1:]
        if not files:
            sys.exit("No ch_*.txt files in %r." % a.dir)

    total_gap = 0
    for fn in files:
        p = fn if os.path.exists(fn) else os.path.join(a.dir, fn)
        s = io.open(p, encoding="utf-8").read()
        assert s.strip(), "empty file: %s" % p
        parts = re.split(r"===CHAPTER (\d+)===", s)
        for i in range(1, len(parts), 2):
            n = int(parts[i])
            body = "\n".join(parts[i + 1].strip("\n").split("\n")[1:])
            w = len(body.split())
            lo, hi = (a.ch1_lo, a.ch1_hi) if n == 1 else (a.lo, a.hi)
            if w < lo:
                total_gap += lo - w
                flag = "SHORT  need +%d" % (lo - w)
            elif w > hi:
                flag = "LONG   cut  -%d" % (w - hi)
            else:
                flag = "ok"
            print("  Ch %-4d %5d  %s" % (n, w, flag))

    if total_gap:
        print("\n  TOTAL SHORTFALL: %d words. Close it in ONE pass (size the top-up at 2x the gap)." % total_gap)
        sys.exit(1)
    print("\n  All in band.")


if __name__ == "__main__":
    main()
