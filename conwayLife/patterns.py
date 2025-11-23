import os

def load_pattern(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Pattern file not found: {file_path}")

    pattern = []
    # Open the pattern file
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()  # Remove whitespace and newline
            if line:  # Skip empty lines
                # Convert 'O' to alive and '.' to dead, build row
                pattern.append(["⬛" if ch == "O" else "⬜" for ch in line])
    # Return the list
    return pattern
