# Serial Novel Engine

**A Claude skill for planning, drafting and quality-checking long serial novels**: webnovel
apps, Kindle Vella, Royal Road, Wattpad, Substack fiction. Anything published a chapter at a
time and read on a phone.

Built from finishing several 200–360 chapter serials. Most of the rules exist because
something broke at chapter 150.

## What it does

- **Plans the whole book first.** One row per chapter, every chapter, before Chapter 1.
- **Two scenes a chapter, a cliff on every chapter, a reader question in the first half.**
- **Three gate scripts** that catch what an editor misses on a phone screen:

| Script | Catches |
|---|---|
| `wc.py` | chapters outside the word band, with the exact gap to close |
| `scenecheck.py` | chapters that turned into essays (<20% dialogue), two in a row, or too many close together |
| `cliche_check.py` | prose em-dashes, stock romance phrases, aphorism scaffolding: the habits readers skim |

## Install

### Claude Code (plugin)
```
/plugin marketplace add chapterforge/serial-novel-engine
/plugin install serial-novel-engine@serial-novel-engine
```

### Claude Code (manual)
Copy `skills/serial-novel-engine/` into `~/.claude/skills/` (or `.claude/skills/` in your project).

### Claude.ai
Download `serial-novel-engine.zip` from the [latest release](../../releases), then upload it
in Settings → Capabilities → Skills.

## Try it

```bash
cd skills/serial-novel-engine/scripts
python scenecheck.py --dir ../../../examples/manuscript ch_001-002.txt
python wc.py --dir ../../../examples/manuscript ch_001-002.txt
```

Needs Python 3.8+. On Windows, use `py` instead of `python` if `python` opens the Microsoft Store.

The example chapters are deliberately short, so the word gate fires. That's how you know it works.

Then ask Claude: *"Use the serial novel engine. Help me plan a 200-chapter enemies-to-lovers
serial."*

## Pro edition

The free edition covers the drafting loop. **Pro** adds the tooling that keeps a 200+
chapter book consistent:

- whole-book **blueprint checker** (every chapter planned, scene plans, clocks, cliff types)
- **reader-question ledger** with the debt rule (no thread goes cold, no more than 10 live)
- **continuity/fact checker** (ages, places, dates, drift warnings, lonely proper nouns)
- **row check** (did the draft do what the plan said?)
- **cliff ladder** and **act-end audit sweeps**
- one-command **new-book setup** and **.docx export**
- the full rulebook: 48 laws, each with the failure that produced it

→ **[Get Pro](YOUR_STORE_LINK)**

## License

MIT for this free edition. See [LICENSE](LICENSE).
