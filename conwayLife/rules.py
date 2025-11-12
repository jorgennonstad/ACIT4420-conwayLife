# conwayLife/rules.py

RULES = []

def rule(func):
    """Decorator to register a rule function."""
    RULES.append(func)
    return func

# -----------------------------
# Helper function
# -----------------------------
def count_alive_neighbors(board, row, col):
    """Count the number of alive neighbors around a cell."""
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < board.rows and 0 <= nc < board.cols:
                if board.grid[nr][nc] == board.ALIVE:
                    count += 1
    return count

# -----------------------------
# Rule 1: Underpopulation
# -----------------------------
@rule
def underpopulation(board, row, col, new_grid):
    """Any live cell with fewer than 2 live neighbors dies."""
    cell = board.grid[row][col]
    if cell != board.ALIVE:
        return
    if count_alive_neighbors(board, row, col) < 2:
        new_grid[row][col] = board.DEAD

# -----------------------------
# Rule 2: Survival
# -----------------------------
@rule
def survival(board, row, col, new_grid):
    """Any live cell with 2 or 3 live neighbors survives."""
    cell = board.grid[row][col]
    if cell != board.ALIVE:
        return
    neighbors = count_alive_neighbors(board, row, col)
    if neighbors == 2 or neighbors == 3:
        new_grid[row][col] = board.ALIVE

# -----------------------------
# Rule 3: Overpopulation
# -----------------------------
@rule
def overpopulation(board, row, col, new_grid):
    """Any live cell with more than 3 live neighbors dies."""
    cell = board.grid[row][col]
    if cell != board.ALIVE:
        return
    if count_alive_neighbors(board, row, col) > 3:
        new_grid[row][col] = board.DEAD

# -----------------------------
# Rule 4: Reproduction
# -----------------------------
@rule
def reproduction(board, row, col, new_grid):
    """Any dead cell with exactly 3 live neighbors becomes alive."""
    cell = board.grid[row][col]
    if cell != board.DEAD:
        return
    if count_alive_neighbors(board, row, col) == 3:
        new_grid[row][col] = board.ALIVE
