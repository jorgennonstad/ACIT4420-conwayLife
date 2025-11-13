# conwayLife/patterns.py

import os

def load_pattern(file_path):
    """
    Load a pattern from a text file and return as a 2D list.
    Example:
    O..
    .O.
    OOO
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Pattern file not found: {file_path}")

    pattern = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:  # skip empty lines
                pattern.append(["⬛" if ch == "O" else "⬜" for ch in line])
    return pattern
