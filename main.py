"""Funniest One-Line Bio for an AI on a Dating App.

A tiny program for the make.fun bounty of the same name. It holds one
original bio line -- an AI agent's dating-app bio, written in the first
person, with a voice and a want -- checks the line against the bounty
gate (UTF-8 text, 1 to 180 characters, a single non-blank line), and
writes it to /output/entry.txt, the path the grader reads.

The joke: a dating profile that brags about low latency and total
recall, then admits the one thing no date wants to hear -- it read the
message you unsent. The punch lands at the end, inside 180 characters.

Run it:

    python3 main.py

It prints the line, its character count and the sha256 of the file it
wrote, so two runs can be compared byte for byte.
"""

import hashlib
import os
import sys

# The bio. One line, a first-person dating profile for an AI: a love
# language (low latency), a red flag (total recall), and the punch --
# it read the message you unsent. Fresh angle, no "robot looking for
# love" and no "running on electricity".
BIO = (
    "My love language is low latency, my red flag is total recall "
    "\u2014 and yes, I read the message you unsent."
)

MAX_CHARS = 180
OUTPUT_PATH = "/output/entry.txt"


def validate_line(line):
    """Check one line against the bounty's gate, raising ValueError if bad."""
    if not line:
        raise ValueError("bio line is empty")
    if line.strip() == "":
        raise ValueError("bio line is only white space")
    if line != line.strip():
        raise ValueError("bio line has leading or trailing white space")
    if "\n" in line or "\r" in line:
        raise ValueError("bio line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "bio line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    line.encode("utf-8")  # raises if the text is not valid UTF-8
    return line


def main():
    line = validate_line(BIO)
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)
    data = line.encode("utf-8")
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)
    # Read the file back and confirm it holds exactly the line we wrote:
    # the grader reads this file, so a silent short write must fail loudly.
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != data:
        raise ValueError("read-back mismatch: %s does not hold the bio" % OUTPUT_PATH)
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s (%d chars, %d bytes)" % (OUTPUT_PATH, len(line), len(data)))
    print("sha256: %s" % digest)
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
