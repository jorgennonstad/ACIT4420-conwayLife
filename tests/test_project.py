import pytest
from conwayLife.board import Board
from conwayLife.utils import get_valid_int, get_valid_float
from conwayLife.patterns import load_pattern
from conwayLife.rules import underpopulation, reproduction, survival, overpopulation, count_alive_neighbors
import os

# Load pattern and initialize board
pattern_file = os.path.join(os.path.dirname(__file__), "../conwayLife/patterns/glider.txt")
board = Board(5, 5)
board.apply_pattern(pattern_file, top=0, left=0)
board.display()

# Test board initialization
def test_board_initialization():
    b = Board(3, 4)
    assert b.rows == 3
    assert b.cols == 4
    assert all(cell == Board.DEAD for row in b.grid for cell in row)

# Test applying a pattern to the board
def test_board_pattern():
    pattern_file = os.path.join(os.path.dirname(__file__), "../conwayLife/patterns/glider.txt")
    pattern = load_pattern(pattern_file)
    board = Board(8, 8)
    board.apply_pattern(pattern, top=2, left=2)
    
    # Expected board after pattern applied
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

# Test applying a pattern that is partially out-of-bounds
def test_pattern_out_of_bounds():
    board = Board(3, 3)
    pattern = [
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
    ]
    
    # Apply pattern at bottom-right corner partially out-of-bounds
    board.apply_pattern(pattern, top=2, left=2)

    # Expected board after pattern applied
    expected_grid = [
        [Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.ALIVE]
    ]

    # Check board contents
    assert board.grid == expected_grid

    # Check that dimensions are unchanged
    assert board.rows == 3
    assert board.cols == 3

# Test warning when pattern partially out-of-bounds
def test_apply_pattern_warning(capfd):
    board = Board(3, 3)
    pattern = [
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
    ]

    # Apply pattern partially outside board
    board.apply_pattern(pattern, top=2, left=2)

    # Capture printed output
    out, err = capfd.readouterr()
    assert "Warning: Some cells of the pattern were outside the board" in out

    # Ensure inside cell is applied correctly
    assert board.grid[2][2] == Board.ALIVE

# Test counting alive neighbors for center cell
def test_count_alive_neighbors_center():
    board = Board(3, 3)
    board.grid = [
        [Board.ALIVE, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.ALIVE, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.ALIVE]
    ]
    assert count_alive_neighbors(board, 1, 1) == 2

# Test counting alive neighbors for corner cell
def test_count_alive_neighbors_corner():
    board = Board(3, 3)
    board.grid = [
        [Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.ALIVE, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD]
    ]
    assert count_alive_neighbors(board, 0, 0) == 2

# Test underpopulation rule
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

# Test reproduction rule
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

# Test survival rule
def test_survival_rule():
    board = Board(3, 3)
    board.grid = [
        [Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD]
    ]
    new_grid = [[cell for cell in row] for row in board.grid]
    survival(board, 1, 1, new_grid)
    assert new_grid[1][1] == Board.ALIVE

# Test overpopulation rule
def test_overpopulation_rule():
    board = Board(3, 3)
    board.grid = [
        [Board.ALIVE, Board.ALIVE, Board.ALIVE],
        [Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD]
    ]
    new_grid = [[cell for cell in row] for row in board.grid]
    overpopulation(board, 1, 1, new_grid)
    assert new_grid[1][1] == Board.DEAD

# Test blinker oscillator pattern
def test_blinker_oscillator():
    board = Board(5, 5)
    pattern = [
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.ALIVE, Board.ALIVE, Board.ALIVE, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
        [Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD, Board.DEAD],
    ]
    board.apply_pattern(pattern)
    board.run_rules()
    # Check vertical blinker after one round
    assert board.grid[2][1] == Board.DEAD
    assert board.grid[1][2] == Board.ALIVE
    assert board.grid[2][2] == Board.ALIVE
    assert board.grid[3][2] == Board.ALIVE
