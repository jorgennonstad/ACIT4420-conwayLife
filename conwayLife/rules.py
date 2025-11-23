RULES = []

def rule(func):
    # Register a rule function
    RULES.append(func)
    return func

def count_alive_neighbors(board, row, col):
    # Count the number of alive neighbors around a cell
    alive_count = 0
    for row_offset in [-1, 0, 1]:
        for col_offset in [-1, 0, 1]:
            if row_offset == 0 and col_offset == 0:
                continue  # skip the cell itself
            neighbor_row = row + row_offset
            neighbor_col = col + col_offset
            if 0 <= neighbor_row < board.rows and 0 <= neighbor_col < board.cols:
                if board.grid[neighbor_row][neighbor_col] == board.ALIVE:
                    alive_count += 1
    return alive_count


@rule
def underpopulation(board, row, col, new_grid):
    # Any live cell with fewer than 2 neighbors dies
    cell = board.grid[row][col]
    if cell != board.ALIVE:
        return
    if count_alive_neighbors(board, row, col) < 2:
        new_grid[row][col] = board.DEAD

@rule
def survival(board, row, col, new_grid):
    # Live cell with 2 or 3 neighbors survives
    cell = board.grid[row][col]
    if cell != board.ALIVE:
        return
    neighbors = count_alive_neighbors(board, row, col)
    if neighbors == 2 or neighbors == 3:
        new_grid[row][col] = board.ALIVE

@rule
def overpopulation(board, row, col, new_grid):
    # Live cell with more than 3 neighbors dies
    cell = board.grid[row][col]
    if cell != board.ALIVE:
        return
    if count_alive_neighbors(board, row, col) > 3:
        new_grid[row][col] = board.DEAD

@rule
def reproduction(board, row, col, new_grid):
    # Dead cell with exactly 3 neighbors becomes alive
    cell = board.grid[row][col]
    if cell != board.DEAD:
        return
    if count_alive_neighbors(board, row, col) == 3:
        new_grid[row][col] = board.ALIVE
