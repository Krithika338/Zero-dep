import re


def tokenize(text):
    """Convert text into lowercase word tokens."""
    return re.findall(r"\b\w+\b", text.lower())