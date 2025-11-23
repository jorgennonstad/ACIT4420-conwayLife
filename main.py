from conwayLife import (
    Board,
    load_pattern,
    clear_console,
    choose_pattern,
    logger,
    get_valid_int,
    get_valid_float,
)

import time

def main():
    # Choose pattern file
    pattern_file = choose_pattern()
    pattern = load_pattern(pattern_file)

    pattern_rows = len(pattern)
    pattern_cols = len(pattern[0])

    # Get board size from user
    while True:
        rows = get_valid_int(f"Enter number of rows (min {pattern_rows + 5}): ")
        cols = get_valid_int(f"Enter number of columns (min {pattern_cols + 5}): ")

        if rows < pattern_rows + 5 or cols < pattern_cols + 5:
            print(f"Board too small! Must be at least "
                  f"{pattern_rows + 5} x {pattern_cols + 5} to fit the pattern.")
        else:
            break

    # Get number of rounds and speed from user
    rounds = get_valid_int("Enter number of rounds: ")
    speed = get_valid_float("Enter speed (seconds per round): ")

    # Create the board
    board = Board(rows, cols)

    # Center the pattern on the board
    top = (board.rows - pattern_rows) // 2
    left = (board.cols - pattern_cols) // 2
    board.apply_pattern(pattern, top=top, left=left)

    # Run the simulation
    for round in range(rounds):
        clear_console()
        print(f"Round {round + 1}:")

        # Log current board state (overwrite file on first round)
        overwrite = (round == 0)
        logger(pattern_file, board, round + 1, overwrite=overwrite)

        # Display board and apply rules for next iteration
        board.display()
        board.run_rules()
        time.sleep(speed)


if __name__ == "__main__":
    main()
