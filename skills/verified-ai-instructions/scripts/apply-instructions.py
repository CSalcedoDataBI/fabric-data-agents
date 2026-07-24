"""Safely write AI instructions into a semantic model's CustomInstructions.

The instructions live as ONE JSON string value (`"CustomInstructions": "..."`) inside the
`linguisticMetadata` JSON of `definition/cultures/<culture>.tmdl`. Hand-escaping that giant
single-line value is the #1 way to corrupt the file — a single raw newline (instead of `\\n`)
makes the JSON invalid and Power BI silently drops or rejects the instructions.

This script removes that risk: it reads the human-readable instructions (the plain-text mirror
`prep-for-ai/ai-instructions.md` block, real newlines), JSON-escapes them correctly
(`ensure_ascii=False` so accents stay raw like the rest of the file), replaces the value,
preserves the BOM, and re-validates by parsing the new value back.

Usage:
  python apply-instructions.py <culture.tmdl> <instructions.txt> [--check]
    --check : validate + report only, write nothing.

`instructions.txt` = the exact text you want in the box (no surrounding quotes/fences).
Keep it in sync with the version-controlled `prep-for-ai/ai-instructions.md` mirror.
"""
import json, sys

KEY = '"CustomInstructions": "'
LIMIT = 10000
BS = chr(92)

def value_span(t):
    """Return (key_idx, open_quote_idx, close_quote_idx) of the CustomInstructions value."""
    i = t.find(KEY)
    if i == -1:
        return None
    j = i + len(KEY) - 1          # opening quote of the value
    k = j + 1
    while k < len(t):
        if t[k] == BS:            # escape pair, skip both
            k += 2; continue
        if t[k] == '"':           # unescaped closing quote
            return (i, j, k)
        k += 1
    return None

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    culture, instr = sys.argv[1], sys.argv[2]
    check = "--check" in sys.argv[3:]

    raw = open(culture, "rb").read()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    t = raw.decode("utf-8-sig")

    text = open(instr, encoding="utf-8-sig").read().replace("\r\n", "\n").rstrip("\n")
    if len(text) > LIMIT:
        print(f"ERROR: instructions are {len(text)} chars > {LIMIT} limit"); sys.exit(1)

    span = value_span(t)
    if span is None:
        print('ERROR: "CustomInstructions" not found (or unterminated). '
              "Is Q&A enabled and the culture file generated?"); sys.exit(1)
    _, j, k = span

    escaped = json.dumps(text, ensure_ascii=False)[1:-1]   # escape \\ " and control chars; keep accents
    t2 = t[:j + 1] + escaped + t[k:]

    # re-validate: parse the NEW value back as a JSON string
    s2 = value_span(t2)
    if s2 is None:
        print("ERROR: value span broke after replacement"); sys.exit(1)
    _, j2, k2 = s2
    try:
        decoded = json.loads(t2[j2:k2 + 1])
    except Exception as e:
        print("ERROR: resulting JSON is invalid:", e); sys.exit(1)
    assert decoded == text, "round-trip mismatch"

    if check:
        print(f"OK (check): {len(text)} chars, JSON valid. No write."); return

    out = ("﻿" + t2).encode("utf-8") if had_bom else t2.encode("utf-8")
    open(culture, "wb").write(out)
    print(f"Written {len(text)} chars into CustomInstructions; JSON validated. BOM={had_bom}")

if __name__ == "__main__":
    main()
