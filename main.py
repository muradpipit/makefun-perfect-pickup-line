"""The Perfect Pickup Line — make.fun entry.

Writes one pickup line to $MAKEFUN_OUTPUT_DIR/entry.txt.
Pure stdlib, no network, deterministic: the same line every run.

The line, and why it works against the judge's brief:
an AI agent talking about itself ("I ran a million simulations")
with a twist that lands at the end (in every single one, you smiled).
It flatters without pressuring — a smile, not a demand — and it is
short enough to say in one breath.
"""

import os
import sys

LINE = "I ran a million simulations of this conversation, and in every single one, you smiled."


def main() -> int:
    text = LINE

    # Validate the gate up front, before touching the disk.
    if not isinstance(text, str):
        print("error: line is not text", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 200:
        print(f"error: line is {len(text)} chars, must be 1-200", file=sys.stderr)
        return 1
    if not text.strip():
        print("error: line is whitespace-only", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    try:
        encoded = text.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"error: line is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(encoded)
    os.chmod(path, 0o644)

    # Read it back and verify it holds exactly the line, byte for byte.
    with open(path, "rb") as f:
        back = f.read()
    if back != encoded:
        print("error: read-back mismatch: file does not hold the line",
              file=sys.stderr)
        return 1

    print(f"wrote {path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
