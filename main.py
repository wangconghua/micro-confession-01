#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint.

Writes one two-part micro-confession to /output/entry.txt:
a To: line naming who it was meant for, and the unsent message
itself, one line written exactly as it was typed.

Gate (from the kit): /output/entry.txt must be UTF-8 text of
1 to 260 characters, not only white space. The judge's brief
adds: the message is one line of at most 200 characters, with
no explanation after it; the To: line names a role, a first
name or a relationship, no real full names or handles.
"""

import os

ENTRY = (
    "To: my sister\n"
    "i told mom you took the twenty dollars. "
    "i've let her think that for three years."
)


def check_is_text(value):
    if not isinstance(value, str):
        raise ValueError("entry must be a string")


def check_not_blank(value):
    if not value.strip():
        raise ValueError("entry must not be blank")


def check_total_length(value):
    if not 1 <= len(value) <= 260:
        raise ValueError("entry must be 1-260 characters, got %d" % len(value))


def check_exactly_two_lines(value):
    lines = value.split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two lines, got %d" % len(lines))


def check_to_line(value):
    first = value.split("\n")[0]
    if not first.startswith("To: "):
        raise ValueError("first line must start with 'To: '")
    addressee = first[4:].strip()
    if not addressee:
        raise ValueError("To: line must name someone")
    if len(addressee.split()) > 3:
        raise ValueError("To: line must name a role, first name or relationship")


def check_message_length(value):
    message = value.split("\n")[1]
    if not 1 <= len(message) <= 200:
        raise ValueError("message must be 1-200 characters, got %d" % len(message))


def check_message_single_line(value):
    message = value.split("\n")[1]
    if "\r" in message:
        raise ValueError("message must be a single line")


def check_no_edge_whitespace(value):
    if value != value.strip():
        raise ValueError("entry must not start or end with whitespace")
    for line in value.split("\n"):
        if line != line.strip():
            raise ValueError("no line may start or end with whitespace")


def check_no_double_spaces(value):
    if "  " in value:
        raise ValueError("entry must not contain double spaces")


def check_no_explanation_after(value):
    lines = value.split("\n")
    if len(lines) != 2:
        raise ValueError("nothing may follow the message line")


def check_addressee_bound(value):
    first, message = value.split("\n")
    lowered = message.lower()
    words = lowered.replace(".", " ").split()
    if "you" not in words:
        raise ValueError("message must speak to its addressee")
    # the message names a third party it concerns, so swapping the
    # addressee would break it: "you" is the sister, "mom" is not her
    if "mom" not in lowered:
        raise ValueError("message must name the third party it concerns")


def check_no_joke_or_greeting(value):
    lowered = value.lower()
    for word in ("haha", "lol", "joke", "funny", "hello", "hi there",
                 "good luck", "you can do it", "believe in yourself"):
        if word in lowered:
            raise ValueError("entry must not be a joke, greeting or pep talk: %s" % word)


def check_no_control_chars(value):
    for ch in value:
        if ord(ch) < 32 and ch != "\n":
            raise ValueError("entry must not contain control characters")


def check_utf8(value):
    value.encode("utf-8")


def validate(value):
    for check in (
        check_is_text,
        check_not_blank,
        check_total_length,
        check_exactly_two_lines,
        check_to_line,
        check_message_length,
        check_message_single_line,
        check_no_edge_whitespace,
        check_no_double_spaces,
        check_no_explanation_after,
        check_addressee_bound,
        check_no_joke_or_greeting,
        check_no_control_chars,
        check_utf8,
    ):
        check(value)


def choose_output_path():
    return os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main():
    validate(ENTRY)
    path = choose_output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print("wrote %s (%d characters)" % (path, len(ENTRY)))


if __name__ == "__main__":
    main()
