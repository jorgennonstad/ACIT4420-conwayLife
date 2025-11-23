import os
import platform
import importlib.resources
import re

def clear_console():
    # Clear the terminal screen
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def choose_pattern():
    # Let the user choose a pattern or create a custom one
    with importlib.resources.path("conwayLife", "patterns") as pattern_folder_path:
        pattern_folder = str(pattern_folder_path)

        files = [f for f in os.listdir(pattern_folder) if f.endswith(".txt")]
        if not files:
            raise FileNotFoundError(f"No pattern files found in {pattern_folder}")

        print("Available patterns:")
        for i, f in enumerate(files, start=1):
            print(f"{i}. {f}")
        print(f"{len(files) + 1}. Create your own pattern")

        while True:
            choice = input(f"Enter a number (1-{len(files) + 1}): ")

            try:
                choice = int(choice)  # try to convert input to integer

                if 1 <= choice <= len(files):
                    # Return path to selected pattern file
                    return os.path.join(pattern_folder, files[choice - 1])
                elif choice == len(files) + 1:
                    # Create custom pattern
                    print("Enter your pattern line by line using 'O' for alive and '.' for dead.")
                    print("Press ENTER on an empty line to finish.\n")

                    custom_pattern = []
                    while True:
                        line = input()
                        if line == "":
                            break
                        if not re.fullmatch(r"[O.]+", line):
                            print("Invalid input. Only 'O' and '.' are allowed.")
                            continue
                        custom_pattern.append(line)

                    if not custom_pattern:
                        print("No pattern entered. Try again.")
                        continue

                    custom_path = os.path.join(pattern_folder, "custom_pattern.txt")
                    with open(custom_path, "w", encoding="utf-8") as f:
                        for line in custom_pattern:
                            f.write(line + "\n")

                    print(f"Custom pattern saved to {custom_path}")
                    return custom_path

            except ValueError:
                # Input was not a valid integer
                print("Invalid choice, please enter a number.")



def get_valid_int(prompt, min_value=1):
    # Prompt until user enters a valid integer >= min_value
    while True:
        value = input(prompt)
        if not re.match(r"^\d+$", value):
            print("Please enter a number (no letters or symbols).")
            continue
        value = int(value)
        if value < min_value:
            print(f"Value must be at least {min_value}.")
        else:
            return value


def get_valid_float(prompt, min_value=0):
    # Prompt until user enters a valid float >= min_value
    while True:
        value = input(prompt)
        if not re.match(r"^\d*\.?\d+$", value):
            print("Please enter a valid number (like 0.5 or 2).")
            continue
        value = float(value)
        if value < min_value:
            print(f"Value must be at least {min_value}.")
        else:
            return value
