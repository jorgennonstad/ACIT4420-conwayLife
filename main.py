from conwayLife import Board
from conwayLife.patterns import load_pattern
from conwayLife import clear_console, choose_pattern
import time

def main():
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    rounds = int(input("Enter number of rounds: "))
    speed = float(input("Enter speed (seconds per round): "))

    board = Board(rows, cols)

    # Let the user choose a pattern
    pattern_file = choose_pattern()
    pattern = load_pattern(pattern_file)

    # Center the pattern on the board
    pattern_rows = len(pattern)
    pattern_cols = len(pattern[0])
    top = (board.rows - pattern_rows) // 2
    left = (board.cols - pattern_cols) // 2

    board.apply_pattern(pattern, top=top, left=left)

    for round in range(rounds):
        clear_console()  # clear before display
        print(f"Round {round + 1}:")
        board.display()
        board.run_rules()
        time.sleep(speed)

if __name__ == "__main__":
    main()
