import importlib.resources
import os
import re
from datetime import datetime

def logger(pattern_path, board, step, overwrite=False):
    # Ensure logs folder inside the package
    with importlib.resources.path("conwayLife", "logs") as logs_folder_path:
        logs_folder = str(logs_folder_path)
        os.makedirs(logs_folder, exist_ok=True)

        match = re.search(r"([^/\\]+)\.txt$", pattern_path)
        pattern_name = match.group(1) if match else pattern_path

        mode = "w" if overwrite else "a"
        log_path = os.path.join(logs_folder, "log.txt")

        with open(log_path, mode, encoding="utf-8") as f:
            f.write(f"----- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----\n")
            f.write(f"Pattern: {pattern_name}, Step: {step}\n")
            for row in board.grid:
                f.write(" ".join(row) + "\n")
            f.write("\n")
