from figure_out_line import get_sure_squares

def solve_picross_simple(all_clues, grid = None):
    #  1 is filled, 3 is empty, 0 is unknown
    X = len(all_clues[0])
    Y = len(all_clues[1])
    if grid is None:
        grid = [[0 for _ in range(X)] for _ in range(Y)]
    
    todo = []
    todo += [(0, c) for c in range(X)]
    todo += [(1, r) for r in range(Y)]
    
    while todo:
        this_todo = todo.pop(0)
        side, index = this_todo
        if side == 0:
            c = index
            clues = all_clues[0][c]
            grid_part = [grid[r][c] for r in range(Y)]
            sol = get_sure_squares(clues, grid_part)
            if sol is False:
                print("Unsolvable line detected at column", c)
                return False
            for r in range(Y):
                if grid[r][c] != sol[r]:
                    todo.append((1, r))
                grid[r][c] = sol[r]
                
        else:
            r = index
            clues = all_clues[1][r]
            grid_part = grid[r]
            sol = get_sure_squares(clues, grid_part)
            if sol is False:
                print("Unsolvable line detected at row", r)
                return False
            for c in range(X):
                if grid[r][c] != sol[c]:
                    todo.append((0, c))
                grid[r][c] = sol[c]
    amount_sure = sum(1 for r in range(Y) for c in range(X) if grid[r][c] in (1,3))
    return grid, amount_sure