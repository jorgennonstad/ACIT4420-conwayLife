from conwayLife import Board
from conwayLife.patterns import load_pattern
from conwayLife.utils import clear_console  # <-- import the helper
import time

def main():
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    rounds = int(input("Enter number of rounds: "))
    speed = float(input("Enter speed (seconds per round): "))

    board = Board(rows, cols)

    pattern_file = "patterns/glider.txt"
    pattern = load_pattern(pattern_file)
    board.apply_pattern(pattern, top=0, left=0)

    for round in range(rounds):
        clear_console()  # <-- clear before display
        print(f"Round {round + 1}:")
        board.display()
        board.run_rules()
        time.sleep(speed)

if __name__ == "__main__":
    main()
