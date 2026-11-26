"""Resignation letter entry for make.fun.

Builds the one-line resignation letter from named fragments, guards it
against the competition gate (1-140 characters, a single line, no control
characters), and writes it to $MAKEFUN_OUTPUT_DIR/entry.txt with a
byte-level read-back check.
"""

import os

MAX_LEN = 140
MIN_LEN = 1


def build_letter():
    """Assemble the resignation line from named parts."""
    opening = "I resign effective immediately"
    escalation = "my agent told the CEO, deleted the database"
    punchline = "git blame says I approved it in ticket #4821"
    return f"{opening} — {escalation}, and {punchline}."


def guard_letter(text):
    """Enforce the gate: 1-140 chars, one line, no control characters."""
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        raise ValueError(
            f"letter is {len(text)} chars, must be {MIN_LEN}-{MAX_LEN}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("letter must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("letter contains control characters")
    # Reject invisible characters that would silently change the entry:
    # zero-width space/joiner, byte-order mark, soft hyphen.
    invisible = {"\u200b", "\u200c", "\u200d", "\ufeff", "\u00ad"}
    if any(ch in invisible for ch in text):
        raise ValueError("letter contains an invisible character")
    if text != text.strip():
        raise ValueError("letter has leading or trailing whitespace")
    return text


def publish(text):
    """Write the letter to $MAKEFUN_OUTPUT_DIR/entry.txt and verify it."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(out_path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        raise ValueError("entry.txt bytes do not match the letter")
    return out_path


def main():
    letter = guard_letter(build_letter())
    path = publish(letter)
    print(f"wrote {len(letter)} chars to {path}")


if __name__ == "__main__":
    main()
