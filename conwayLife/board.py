from conwayLife.rules import RULES



class Board:
    DEAD = "⬜"   # empty / dead
    ALIVE = "⬛"  # filled / alive

    def __init__(self, rows, cols):
        # Make sure board dimensions are positive
        if rows <= 0 or cols <= 0:
            raise ValueError("Board dimensions must be positive integers.")
        self.rows = rows
        self.cols = cols
        self.grid = self.create_board()  # initialize the grid

    def create_board(self):
        # Create a grid filled with DEAD cells
        grid = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(self.DEAD)
            grid.append(row)
        return grid

    def display(self):
        # Print the current state of the board
        for r in range(self.rows):
            line = ""
            for c in range(self.cols):
                line += self.grid[r][c] + " "
            print(line)

    def apply_pattern(self, pattern, top=0, left=0):
        # Place a pattern on the board at the given position
        out_of_bounds = False
        row_index = 0
        for row in pattern:
            col_index = 0
            for cell in row:
                board_row = top + row_index
                board_col = left + col_index

                # Only place cells inside the board
                if board_row >= 0 and board_row < self.rows and board_col >= 0 and board_col < self.cols:
                    self.grid[board_row][board_col] = cell
                else:
                    out_of_bounds = True  # mark if pattern goes outside


                col_index += 1
            row_index += 1

        # Warn if some cells were outside the board
        if out_of_bounds:
            print("Warning: Some cells of the pattern were outside the board")

    def run_rules(self):
        # Apply all registered rules simultaneously
        # Start with a new grid filled with DEAD cells
        new_grid = [[self.DEAD for col_index in range(self.cols)] for row_index in range(self.rows)]

        # Copy current grid to new grid
        for r in range(self.rows):
            for c in range(self.cols):
                new_grid[r][c] = self.grid[r][c]

        # Apply each rule to every cell
        for r in range(self.rows):
            for c in range(self.cols):
                for rule_func in RULES:
                    rule_func(self, r, c, new_grid)

        # Update the board with the new grid after rules applied
        self.grid = new_grid
