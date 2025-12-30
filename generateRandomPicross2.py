import random
from picrossSolver import solve_picross_simple

def get_clues_from_grid(grid):
    x = len(grid[0])
    y = len(grid)
    # Function to calculate clues for a single line (row or column)
    def calculate_clues(line):
        clues = []
        count = 0
        for cell in line:
            if cell == 1:
                count += 1
            else:
                if count > 0:
                    clues.append(count)
                    count = 0
        if count > 0:
            clues.append(count)
        return clues if clues else []

    # Calculate row clues
    row_clues = [calculate_clues(row) for row in grid]

    # Calculate column clues
    column_clues = [calculate_clues([grid[row][col] for row in range(y)]) for col in range(x)]
    
    return [row_clues, column_clues]

def generate_random_clues_2(x, y, Ades):
    grid = [[1 for _ in range(x)] for _ in range(y)]
        
    def av_clues_length(row_clues, col_clues):
        total = sum(len(rc) for rc in row_clues) + sum(len(cc) for cc in col_clues)
        count = len(row_clues) + len(col_clues)
        return total / count if count > 0 else 0

    for _ in range(100000):
        grid[random.randrange(y)][random.randrange(x)] = 3
        clues = get_clues_from_grid(grid)
        g, am_s = solve_picross_simple(clues)
        if not g or am_s < x * y:
            grid[random.randrange(y)][random.randrange(x)] = 1
        A = av_clues_length(clues[0], clues[1])
        # print(A)
        if A > Ades:
            return clues, grid
    
if __name__ == "__main__":
    x = 20
    y = 20
    Ades = 3
    print(generate_random_clues_2(x, y, Ades))