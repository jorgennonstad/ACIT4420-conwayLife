import importlib.resources
import os
import re
from datetime import datetime

def logger(pattern_path, board, step, overwrite=False):
    # makes sure the 'logs' folder exists inside the package
    with importlib.resources.path("conwayLife", "logs") as logs_folder_path:
        logs_folder = str(logs_folder_path)
        os.makedirs(logs_folder, exist_ok=True)

        # Gets the pattern file name without extension or filepath
        match = re.search(r"([^/\\]+)\.txt$", pattern_path)
        pattern_name = match.group(1) if match else pattern_path

        # Chose file mode: overwrite or append
        mode = "w" if overwrite else "a"
        log_path = os.path.join(logs_folder, "log.txt")

        # Write the current board state to the log file
        with open(log_path, mode, encoding="utf-8") as f:
            # Write timestamp and step information
            f.write(f"----- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----\n")
            f.write(f"Pattern: {pattern_name}, Step: {step}\n")
            
            # Write the board rows
            for row in board.grid:
                f.write(" ".join(row) + "\n")
            
            # Add a blank line after each step
            f.write("\n")
