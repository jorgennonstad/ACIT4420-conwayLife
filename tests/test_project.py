import pytest
from conwayLife.board import Board
from conwayLife.utils import get_valid_int
from conwayLife.patterns import load_pattern
from conwayLife.rules import underpopulation, reproduction, survival, overpopulation, count_alive_neighbors
import os


pattern_file = os.path.join(os.path.dirname(__file__), "../conwayLife/patterns/glider.txt")
board = Board(5, 5)
board.apply_pattern(pattern_file, top=0, left=0)

board.display()



def test_board_initialization():
    b = Board(3, 4)
    assert b.rows == 3
    assert b.cols == 4
    assert all(cell == Board.DEAD for row in b.grid for cell in row)



def test_board_pattern():
    pattern_file = os.path.join(os.path.dirname(__file__), "../conwayLife/patterns/glider.txt")
    pattern = load_pattern(pattern_file)
    board = Board(8, 8)
    board.apply_pattern(pattern, top=2, left=2)  # adjust until it matches expected_grid
    
    expected_grid = [
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.ALIVE, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.ALIVE, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.ALIVE, Board.ALIVE, Board.ALIVE, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
    ]
    assert board.grid == expected_grid



def test_pattern_out_of_bounds():
    board = Board(3, 3)
    pattern = [
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
    ]
    board.apply_pattern(pattern, top=2, left=2)  # bottom-right corner partially out
    assert board.grid[2][2] == Board.ALIVE


def test_pattern_out_of_bounds_safe():
    board = Board(3, 3)
    pattern = [
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
    ]
    board.apply_pattern(pattern, top=2, left=2)  # bottom-right corner partially out

    # The only cell that should change is (2,2)
    expected_grid = [
        [Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.ALIVE],
    ]
    assert board.grid == expected_grid



def test_apply_pattern_warning(capfd):
    board = Board(3, 3)
    pattern = [
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
    ]

    # Apply pattern partially outside the board
    board.apply_pattern(pattern, top=2, left=2)

    # Capture printed output
    out, err = capfd.readouterr()
    assert "⚠️ Warning: Some cells of the pattern were outside the board" in out

    # Ensure the inside cell is still applied correctly
    assert board.grid[2][2] == Board.ALIVE



def test_board_min_size(monkeypatch):
    pattern_file = os.path.join(os.path.dirname(__file__), "../conwayLife/patterns/glider.txt")
    pattern = load_pattern(pattern_file)
    pattern_rows = len(pattern)
    pattern_cols = len(pattern[0])
    
    # Simulate user entering invalid sizes first, then a valid one
    # For example, glider is 3x3 → min rows/cols = 3+5=8
    inputs = iter(["5", "7", "8", "6", "8"])  # first rows invalid, then cols invalid, then both valid
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    # Test rows
    rows = get_valid_int(f"Enter number of rows (min {pattern_rows + 5}): ", min_value=pattern_rows + 5)
    assert rows >= pattern_rows + 5
    
    # Test cols
    cols = get_valid_int(f"Enter number of columns (min {pattern_cols + 5}): ", min_value=pattern_cols + 5)
    assert cols >= pattern_cols + 5




def test_count_alive_neighbors_center():
    board = Board(3, 3)
    board.grid = [
        [Board.ALIVE, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.ALIVE, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.ALIVE]
    ]
    # center cell at (1,1) has 2 alive neighbors
    assert count_alive_neighbors(board, 1, 1) == 2

def test_count_alive_neighbors_corner():
    board = Board(3, 3)
    board.grid = [
        [Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.ALIVE, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD]
    ]
    # top-left corner (0,0) has 2 alive neighbors
    assert count_alive_neighbors(board, 0, 0) == 2

# -----------------------------
# Example: test underpopulation rule
# -----------------------------
def test_underpopulation_rule():
    board = Board(3, 3)
    board.grid = [
        [Board.ALIVE, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.ALIVE],
        [Board.DEAD, Board.ALIVE, Board.ALIVE]
    ]
    new_grid = [[cell for cell in row] for row in board.grid]
    underpopulation(board, 0, 0, new_grid)
    assert new_grid[1][1] == Board.DEAD

# -----------------------------
# Example: test reproduction rule
# -----------------------------
def test_reproduction_rule():
    board = Board(3, 3)
    board.grid = [
        [Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.ALIVE, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD]
    ]
    new_grid = [[cell for cell in row] for row in board.grid]
    reproduction(board, 1, 1, new_grid)
    assert new_grid[1][1] == Board.ALIVE



def test_survival_rule():
    board = Board(3, 3)
    board.grid = [
        [Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD]
    ]
    new_grid = [[cell for cell in row] for row in board.grid]

    # Apply survival rule to center cell (1,1)
    survival(board, 1, 1, new_grid)

    # center cell survives because it has 3 alive neighbors
    assert new_grid[1][1] == Board.ALIVE


def test_overpopulation_rule():
    board = Board(3, 3)

    board.grid = [
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
        [Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD]
    ]
    new_grid = [[cell for cell in row] for row in board.grid]

    overpopulation(board, 1, 1, new_grid)

    # Center cell dies because it has 4 alive neighbors (>3)
    assert new_grid[1][1] == Board.DEAD



def test_blinker_oscillator():
    board = Board(5, 5)
    # Horizontal blinker
    pattern = [
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.ALIVE, Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
    ]
    board.apply_pattern(pattern)
    board.run_rules()
    # After 1 round, blinker should be vertical
    assert board.grid[2][1] == Board.DEAD
    assert board.grid[1][2] == Board.ALIVE
    assert board.grid[2][2] == Board.ALIVE
    assert board.grid[3][2] == Board.ALIVE
