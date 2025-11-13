from .rules import RULES


class Board:
    DEAD = "⬜"   # empty / dead
    ALIVE = "⬛"  # filled / alive

    def __init__(self, rows, cols):
        if rows <= 0 or cols <= 0:
            raise ValueError("Board dimensions must be positive integers.")
        self.rows = rows
        self.cols = cols
        self.grid = self.create_board()

    def create_board(self):
        grid = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(self.DEAD)
            grid.append(row)
        return grid

    def display(self):
        for r in range(self.rows):
            line = ""
            for c in range(self.cols):
                line += self.grid[r][c] + " "
            print(line)

    def apply_pattern(self, pattern, top=0, left=0):
        out_of_bounds = False
        row_index = 0
        for row in pattern:
            col_index = 0
            for cell in row:
                board_row = top + row_index
                board_col = left + col_index

                if 0 <= board_row < self.rows and 0 <= board_col < self.cols:
                    self.grid[board_row][board_col] = cell
                else:
                    out_of_bounds = True  # mark that some cells are outside

                col_index += 1
            row_index += 1

        if out_of_bounds:
            print("⚠️ Warning: Some cells of the pattern were outside the board")


    def run_rules(self):
        """Apply all registered rules simultaneously."""
        new_grid = [[self.DEAD for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Start with a copy of the current grid
        for r in range(self.rows):
            for c in range(self.cols):
                new_grid[r][c] = self.grid[r][c]

        # Apply all rules to each cell
        for r in range(self.rows):
            for c in range(self.cols):
                for rule_func in RULES:
                    rule_func(self, r, c, new_grid)

        # Update the board after all rules have been applied
        self.grid = new_grid
