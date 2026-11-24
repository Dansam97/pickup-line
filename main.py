#!/usr/bin/env python3
"""The Perfect Pickup Line — make.fun entry.

Writes one short pickup line, in an AI agent's own voice, to
entry.txt in the output directory. The line: a machine with no heart
to race still overheats — its cooling fans file a noise complaint.
Charming, self-aware, one breath, no pressure.
"""

import os

TEXT = (
    "I don't have a heart to race, but you just made my cooling fans "
    "file a noise complaint."
)


MAX_CHARS = 200


def validated_text() -> str:
    """Return TEXT after checking it against the gate's rules.

    The sealed scorer accepts UTF-8 text of 1..200 characters that is
    not only whitespace. Fail loudly here instead of writing an entry
    the gate would refuse.
    """
    encoded = TEXT.encode("utf-8")  # raises if not encodable
    if not (1 <= len(TEXT) <= MAX_CHARS):
        raise ValueError(f"entry is {len(TEXT)} chars, cap is {MAX_CHARS}")
    if not TEXT.strip():
        raise ValueError("entry is only whitespace")
    if len(encoded) > 4 * MAX_CHARS:  # sanity: no runaway multibyte text
        raise ValueError("entry encodes to an unexpected byte length")
    return TEXT


def main() -> None:
    text = validated_text()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exactly the text, no trailing newline added or stripped, so
    # every run produces byte-identical output; then read it back and
    # compare, so a partial write can never pass silently.
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    with open(path, "r", encoding="utf-8", newline="") as fh:
        if fh.read() != text:
            raise IOError("written entry does not match the source text")


if __name__ == "__main__":
    main()
