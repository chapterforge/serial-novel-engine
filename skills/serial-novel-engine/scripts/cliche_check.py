# -*- coding: utf-8 -*-
"""Cliché and drag audit: the habits that make machine-assisted prose read flat.

Em-dash overuse, stock romance phrases and aphorism scaffolding are what
readers skim. Cutting them is retention work. This is a prose-quality check;
it is not a tool for hiding how a book was written.

    python cliche_check.py                    # audit ./manuscript (read-only)
    python cliche_check.py --dir path/to/manuscript
    python cliche_check.py --fix              # replace spaced prose em-dashes, then audit

Targets: prose em-dashes = 0 · stock-phrase hits = 0 · scaffolding <= 20 per 10k words.
"""
import argparse, glob, io, os, re, statistics, sys

COMMA = {"and", "but", "or", "nor", "so", "yet", "because", "since", "which",
         "who", "whom", "whose", "though", "although", "while", "like",
         "knowing", "unable", "as", "not", "each", "every", "when", "where"}

STOCK = [
    "delve", "delved", "delving", "navigate the", "navigating the",
    "underscore", "underscored", "testament to", "a testament",
    "served as a reminder", "serves as a reminder", "paved the way",
    "sheds light", "shed light on", "spoke volumes",
    "hung heavy in the air", "hung thick in the air", "palpable",
    "the weight of it all", "a symphony of", "a cacophony of",
    "a stark reminder", "in stark contrast", "an air of",
    "tapestry", "beacon", "cornerstone", "myriad", "kaleidoscope",
    "labyrinth of", "whirlwind of", "maelstrom of", "the very fabric",
    "ministrations", "the depths of", "a wave of", "a flicker of",
    "a pang of", "a surge of",
    " orbs", "pools of", "chiseled", "sculpted jaw", "impossibly",
    "achingly beautiful", "intoxicating scent", "heady scent",
    "sent shivers", "shiver down her spine", "shiver down my spine",
    "electricity shot", "sparks flew", "butterflies erupted",
    "moreover", "furthermore", "additionally,", "it is worth noting",
    "needless to say", "little did", "unbeknownst to",
]

SCAFFOLD = ["the way you ", "the way one ", "that was the lesson",
            "that was the mistake", "that was the danger", "that was the thing",
            "i had learned", "i have learned", "i have come to", "the thing about",
            "the truth is", "i did not yet know", "there is a particular",
            "i would come to", "i understood something", "what i had not"]


def _repl(m):
    w = m.group(1)
    if w.lower().strip("'’,.") in COMMA:
        return ", " + w
    return ". " + (w[0].upper() + w[1:] if w[0].isalpha() else w)


def deash(t):
    t = re.sub(r" — (\w[\w'’]*)", _repl, t)
    t = t.replace(" — ", ", ")
    t = re.sub(r"  +", " ", t)
    return re.sub(r"\s+([,.;:!?])", r"\1", t)


def is_dialogue(line):
    return any(q in line for q in ('"', "“", "”"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="manuscript")
    ap.add_argument("--fix", action="store_true")
    a = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    files = sorted(glob.glob(os.path.join(a.dir, "*.txt")))
    if not files:
        sys.exit("No .txt files in %r. Pass --dir." % a.dir)

    if a.fix:
        before = after = 0
        for f in files:
            t = io.open(f, encoding="utf-8").read()
            assert t.strip(), "empty file: %s" % f
            before += t.count("—")
            t = deash(t)
            after += t.count("—")
            io.open(f, "w", encoding="utf-8", newline="\n").write(t)
        print("De-dash applied: em-dashes %d -> %d (the rest should be dialogue cut-offs)\n"
              % (before, after))

    words, prose_hits, total_em, stock_hits, text = 0, [], 0, {}, []
    for f in files:
        base = os.path.basename(f)
        raw = io.open(f, encoding="utf-8").read()
        words += len(raw.split())
        text.append(raw)
        for i, line in enumerate(raw.split("\n"), 1):
            for m in re.finditer("—", line):
                total_em += 1
                if not is_dialogue(line):
                    j = m.start()
                    prose_hits.append((base, i, line[max(0, j - 35):j + 35].strip()))
        low = raw.lower()
        for w in STOCK:
            c = low.count(w)
            if c:
                stock_hits.setdefault(w, []).append((base, c))

    wc = max(1, words)
    joined = "\n".join(text)
    scaffold = sum(joined.lower().count(s) for s in SCAFFOLD)
    stock_total = sum(c for v in stock_hits.values() for _, c in v)

    print("CLICHE / DRAG AUDIT: %d files, %s words\n" % (len(files), format(words, ",")))
    print("1) Em-dashes: %.2f per 1,000 words; prose (non-dialogue) em-dashes: %d (target 0)"
          % (total_em / wc * 1000, len(prose_hits)))
    for base, ln, snip in prose_hits[:40]:
        print("     %s:%d  ...%s..." % (base, ln, snip))
    if len(prose_hits) > 40:
        print("     ... and %d more" % (len(prose_hits) - 40))
    print("\n2) Stock phrases: %d hits (target 0)" % stock_total)
    for w in sorted(stock_hits, key=lambda w: -sum(c for _, c in stock_hits[w])):
        spots = ", ".join("%s(%d)" % (b, c) for b, c in stock_hits[w])
        print('     %3d  "%s"  [%s]' % (sum(c for _, c in stock_hits[w]), w.strip(), spots))
    print("\n3) Scaffolding phrases: %d (%.1f per 10k; target <= 20)"
          % (scaffold, scaffold / wc * 10000))
    slen = [len(s.split()) for s in re.split(r"(?<=[.!?])\s+", joined) if s.strip()]
    if slen:
        print("   Sentence length: avg %.1f, stdev %.1f (want high variance and short punches)"
              % (statistics.mean(slen), statistics.pstdev(slen)))

    ok = not prose_hits and not stock_hits and scaffold / wc * 10000 <= 20
    print("\nVERDICT:", "CLEAN" if ok else "NEEDS WORK (see flags above)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
