import random

def generate_random_clues(x, y, Mmax, Amax, grid=None):
    def generate_random_picross(x, y, grid=None):
        if grid is None:
                # Create a grid filled with random 0s and 1s
                grid = [[random.randint(0, 1) for _ in range(x)] for _ in range(y)]
                grid = [[1 if random.random() < 0.75 else 0 for _ in range(x)] for _ in range(y)]

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

        return grid, row_clues, column_clues

    g, r, c = generate_random_picross(x, y)

    def max_clues_length(row_clues, col_clues):
        return max(max((len(rc) for rc in row_clues), default=0),
                max((len(cc) for cc in col_clues), default=0))
        
    def av_clues_length(row_clues, col_clues):
        total = sum(len(rc) for rc in row_clues) + sum(len(cc) for cc in col_clues)
        count = len(row_clues) + len(col_clues)
        return total / count if count > 0 else 0

    M = max_clues_length(r, c)
    A = av_clues_length(r, c)
    iters = 0
    max_iters = 1000000

    lowest_M = 100
    lowest_A = 100
    while (M > Mmax or A > Amax) and iters < max_iters:
        row_lens = [len(rc) for rc in r]
        col_lens = [len(cc) for cc in c]
        max_row = max(row_lens) if row_lens else 0
        max_col = max(col_lens) if col_lens else 0
        overall_max = max(max_row, max_col)

        choices = []
        if max_row == overall_max:
            choices.extend(('row', i) for i, l in enumerate(row_lens) if l == max_row)
        if max_col == overall_max:
            choices.extend(('col', i) for i, l in enumerate(col_lens) if l == max_col)
        # also add a random row or col:
        choices.append( ('row', random.randrange(y)) )
        choices.append( ('col', random.randrange(x)) )

        typ, idx = random.choice(choices)

        if typ == 'row':
            j = random.randrange(x)
            g[idx][j] = 1 - g[idx][j]
        else:
            i = random.randrange(y)
            g[i][idx] = 1 - g[i][idx]

        g, r, c = generate_random_picross(x, y, g)
        M = max_clues_length(r, c)
        A = av_clues_length(r, c)
        if M < lowest_M:
            lowest_M = M
        if A < lowest_A:
            lowest_A = A
        # print(f"{M}/{Mmax}, {A:.2f}/{Amax} (lowest: {lowest_M}, {lowest_A:.2f})")
        iters += 1
    if iters == max_iters:
        # print("Warning: max iters reached in generate_random_clues")
        return False
    return [r,c]
    # with open('picross_clues.txt', 'w', encoding='utf-8') as f:
    #     f.write(f"{r}")
    #     f.write('\n')    
    #     f.write(f"{c}")