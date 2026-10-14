---
name: serial-novel-engine
description: Plan, draft and quality-gate long serial novels (webnovel apps, Kindle Vella, Royal Road, Wattpad, Substack fiction) chapter by chapter. Use when the user wants to outline a serial novel, draft chapters in batches, keep a 100+ chapter book consistent, end every chapter on a cliffhanger, fix chapters that "drag" or read like an essay, or check word counts and AI-sounding clichés in a manuscript.
---

# Serial Novel Engine

A production method for long serial fiction, built from finishing several 200–360 chapter
novels. The core idea: **long books fail from planning and consistency, not from prose.**
So the work runs in three stages, and the scripts in `scripts/` check what a human
editor misses at chapter 150.

Read `references/craft-laws.md` before planning a new book. Read
`references/manuscript-format.md` before writing the first chapter file.

## The three stages (always in this order)

### Stage A: before a word is written
1. **The whole book is planned before Chapter 1.** One row per chapter, to the last
   chapter: date in story time, the beat, POV, the cliff it ends on, and which reader
   question it opens, sharpens or pays. Planning "one act ahead" is how a premise ends
   up in the wrong chapter and gets found 180 chapters late.
2. **The premise sits inside the free sample.** Whatever the platform's free chapters
   are, the hook and the premise land inside them. Check the platform's real paywall
   setting before planning; do not assume.
3. **Before each batch:** read the rows for the batch and the row on either side, then
   **re-read the earlier chapters the batch depends on.** Trust the manuscript, not
   your notes about it. The best callbacks come from what is already on the page.
4. **Set the word target before drafting** (default band 1,000–1,150 words a chapter;
   Chapter 1 runs 1,800–2,200). Aim at the top of the band on the first pass.

### Stage B: writing
- **Two scenes per chapter, planned in the outline.** Default shape: a short lead-in
  scene (300–400 words) that changes something small (a fact, a relationship, a piece of
  information, never only atmosphere), then the planned beat (650–750 words) that ends on
  the cliff. Set pieces can be one scene with a turn in the middle. Never three scenes:
  at this length that reads as summary with scene breaks.
- **Scene, not essay.** Put the protagonist in a room, at an hour, with someone else in
  it, and let that person say something she did not expect. Reflection frames a scene; it
  is never the content of one.
- **Plant a question in the first half.** Name a thing and withhold what it means (a
  ring, a name on a notice, a box with the lid shut, a countdown). The reader should
  finish the chapter wanting an answer she does not have.
- **End on a turn, in the last four lines.** Never on reflection, summary or a settled
  feeling. Vary the kind of cliff so no two in a row are the same type.
- **Voice:** let the narrator be a mess at the wound points. No prose em-dashes, no
  aphorism scaffolding ("The thing about grief is..."), no stock romance phrases. These
  are what make AI-assisted prose drag, and readers skim them.
- **Never write facts from memory.** Ages, dates, place names and who-knows-what get
  checked against the plan before they go on the page.

### Stage C: gates, after every batch
Run these against the manuscript folder (default `./manuscript`, override with `--dir`):

```bash
python scripts/wc.py ch_041-044.txt          # word count per chapter + gap to band
python scripts/scenecheck.py                 # scene-vs-essay gate across the book
python scripts/cliche_check.py               # em-dashes, stock phrases, scaffolding
```

| Gate | Pass condition |
|---|---|
| Word band | every chapter inside the band; a short chapter gets ONE top-up sized at 2x the gap |
| Scene gate | a chapter with <20% dialogue paragraphs is an essay; never two in a row; max 1 in any 4 |
| Cliché gate | prose em-dashes = 0; stock-phrase hits = 0; scaffolding ≤ 20 per 10k words |

A batch is not done until all three pass. Fix flags with craft: replace interiority with
a concrete beat. Never fix with find-and-replace and never pad a finished scene
(weather, "she said slowly") to reach a count.

## How to run a session with the user
1. Ask which book and which chapters. If there is no chapter-by-chapter plan, **stop
   and build the plan first.** Do not invent the next arc when the user types "continue".
2. Do Stage A out loud in two or three lines: the rows, the dependencies you re-read, the
   target.
3. Draft the batch (2–4 chapters) into one file in the format from
   `references/manuscript-format.md`.
4. Run the three gates. Report in one line: chapters, words, gates. Then list only the
   decisions the user needs to make.

## Limits of this free edition
This skill covers the drafting loop. It does not include the whole-book blueprint
checker, the continuity/fact checker, the reader-question ledger, the act-end audit
sweeps, or the platform export builders. Those are in the Pro edition (see README).
