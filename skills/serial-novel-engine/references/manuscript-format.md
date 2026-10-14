# Manuscript format

One file per batch, named `ch_<first>-<last>.txt` (zero-padded is fine: `ch_041-044.txt`),
in the manuscript folder (default `./manuscript`).

```
===CHAPTER 41===
The Ring in the Drawer

First paragraph of the chapter.

"Dialogue paragraphs start with a straight double quote," she said.

Paragraphs are separated by one blank line.

===CHAPTER 42===
Next Title
...
```

Rules:
- `===CHAPTER N===` on its own line opens each chapter. No `.5` chapters.
- The line after the marker is the chapter title; then a blank line; then the body.
- Paragraphs are separated by a blank line. The scene gate counts a paragraph as
  dialogue when it starts with `"`.
- Do not leave an empty header for the next chapter at the end of a file.
- Save as UTF-8 with LF line endings.
- No markdown in prose (`**bold**` leaks into the published text).
