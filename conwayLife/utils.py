import os
import platform

def clear_console():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
