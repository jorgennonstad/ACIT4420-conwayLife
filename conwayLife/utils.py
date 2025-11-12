import os
import platform

def clear_console():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def choose_pattern(pattern_folder="patterns"):
    """Let the user choose a pattern from a folder."""
    files = [f for f in os.listdir(pattern_folder) if f.endswith(".txt")]
    if not files:
        raise FileNotFoundError(f"No pattern files found in {pattern_folder}")

    print("Available patterns:")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {f}")

    while True:
        choice = input(f"Enter a number (1-{len(files)}): ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(files):
                return os.path.join(pattern_folder, files[choice - 1])
        print("Invalid choice, try again.")
