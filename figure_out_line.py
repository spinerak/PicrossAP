import pprint

def get_sure_squares(clues, grid_line):
    # quick handle: all-unknown clues and an empty line
    if all(c == '?' for c in clues):
        if all(g == 0 for g in grid_line):
            if len(clues) * 2 - 1 < len(grid_line):
                return grid_line
            elif len(clues) * 2 - 1 == len(grid_line):
                return [1 if i % 2 == 0 else 0 for i in range(len(grid_line))]
            else:
                print("Unsolvable line detected with all-unknown clues and empty line", clues, grid_line)
                return False
            
    def all_configurations(clues, m, max_QM):        
        n = len(clues)
        if n == 0:
            return [[]]

        # minimal length for each clue ( '?' -> 1, otherwise numeric )
        min_lengths = []
        max_lengths = []
        for c in clues:
            if c == '?':
                min_lengths.append(1)
                max_lengths.append(max_QM)  # theoretically unbounded
            else:
                min_lengths.append(int(c))
                max_lengths.append(int(c))

        configs = []
        curr = []

        def backtrack(idx, pos_min):
            if idx == n:
                configs.append(curr.copy())
                return

            # minimal total length required from idx..end (including 1-space between blocks)
            remaining_blocks = n - idx
            min_total_from_idx = sum(min_lengths[idx:]) + max(0, remaining_blocks - 1)
            max_start = len(grid_line) - min_total_from_idx

            for s in range(pos_min, max_start + 1):
                if clues[idx] != '?':
                    length = int(clues[idx])
                    curr.append([s, length])
                    backtrack(idx + 1, s + length + 1)
                    curr.pop()
                else:
                    # compute minimal total AFTER current block
                    if idx == n - 1:
                        min_after = 0
                    else:
                        min_after = sum(min_lengths[idx + 1:]) + max(0, (n - idx - 1) - 1)
                    max_len = len(grid_line) - s - min_after
                    for length in range(min_lengths[idx], min(max_lengths[idx], max_len) + 1):
                        curr.append([s, length])
                        backtrack(idx + 1, s + length + 1)
                        curr.pop()

        backtrack(0, 0)
        return configs
    
    for max_QM in [1, 2, len(grid_line)]:

        configs = all_configurations(clues, len(grid_line), max_QM)
        
        

        def write_out_configuration(configs, m):
            valid_configs = []
            for config in configs:
                line = [3] * m
                for start, length in config:
                    for i in range(start, start + length):
                        line[i] = 1
                valid_configs.append(line)
            return valid_configs
        
        squares = write_out_configuration(configs, len(grid_line))
        
        valid_configs = []
        for square in squares:
            # compare with grid_line, OK if there is no conflict (one is 1 where the other is 3)
            conflict = any((g != 0 and g != v) for v, g in zip(square, grid_line))
            if not conflict:
                valid_configs.append(square)

            squares = valid_configs
        
        # this is possible if max_QM is too small. if it happens with max_QM == len(grid_line), the puzzle is unsolvable
        # which will be treated at the end where we return False.
        if not valid_configs:  
            continue
        
        # check all entries in valid_configs, if all have 1 in the same position, mark that position as 1, if all have 3 in the same position, mark that position as 3, else 0
        sure_squares = []
        for i in range(len(grid_line)):
            all_ones = all(square[i] == 1 for square in squares)
            all_threes = all(square[i] == 3 for square in squares)
            if all_ones:
                sure_squares.append(1)
            elif all_threes:
                sure_squares.append(3)
            else:
                sure_squares.append(0)
                
        if max_QM < len(grid_line):
            if sure_squares == grid_line:
                # print("No progress can be made with max_QM=", max_QM)
                return sure_squares
        if max_QM == len(grid_line):
            # print("Progress with max_QM=len(grid_line)")
            return sure_squares
    return False

if __name__ == "__main__":
    print(get_sure_squares(['?', 4, '?', 2], [0,0,0,1,0,0,0,0,0,0,1,0,0,3,0]))