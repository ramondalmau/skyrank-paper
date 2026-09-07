"""Detect the LaTeX comment trap: a % block that has swallowed the head of a
sentence, leaving the next live line starting lower-case mid-sentence."""
import re, sys, pathlib

CONT = re.compile(r"^[a-z]")           # live line starting lower case
OK_TAIL = re.compile(r"[,;:a-zA-Z0-9)\-]$")   # previous live line continues

for path in sys.argv[1:]:
    lines = pathlib.Path(path).read_text().split("\n")
    prev_live, prev_live_no = None, None
    hits = 0
    for i, ln in enumerate(lines, 1):
        st = ln.strip()
        if not st:
            prev_live = None
            continue
        if st.startswith("%"):
            continue
        # a live line following one or more comment lines
        j = i - 2
        had_comment = False
        while j >= 0 and lines[j].strip().startswith("%"):
            had_comment = True
            j -= 1
        if had_comment and CONT.match(st):
            # the last live line before the comment block
            before = lines[j].strip() if j >= 0 else ""
            print(f"{path}:{i}: SUSPECT lower-case line after a comment block")
            print(f"    before comment : {before[-70:]}")
            print(f"    comment tail   : {lines[i-2].strip()[-70:]}")
            print(f"    live line      : {st[:70]}")
            hits += 1
        prev_live, prev_live_no = st, i
    print(f"{path}: {hits} suspect site(s)")
