import ast
from pathlib import Path
import random
from random import choice
import copy

from tqdm import tqdm

from generateRandomPicross import generate_random_clues
from generateRandomPicross2 import generate_random_clues_2

from gen_list_of_puzzles import make_lists_of_puzzles
import json

from picrossSolver import solve_picross_simple




def build_up_game(clues):
    """
    Build up the game state from clues.
    Start with all clue entries replaced by "?" and report how many cells can be
    determined. Then repeatedly pick a random "?" and replace it with the actual
    number from `clues`, re-solve, and report the number of filled/empty cells
    after each replacement and which clue was changed.

    Returns a list of step records: dicts with keys
      - step: int (0 = initial masked state)
      - changed: None or (side, line_index, pos_index, value) where side 0=top,1=left
      - marked: number of marked cells after solving
      - masked_clues: deep copy of the current masked clues
    """

    # deep copy original clues to avoid mutating caller data
    orig = [ [list(cl) for cl in part] for part in (clues[0], clues[1]) ]
    
    sss = solve_picross_simple(orig)
    print("Picross solved successfully")
    if sss is False:
        return False
    SOL, N = sss
    
    # if SOL doesn't contain any 0s:
    if N == len(clues[0]) * len(clues[1]):
        print("The provided clues lead to a unique solution!")
        showSolution(SOL)
        pass
    else:
        print("The provided clues do not lead to a unique solution.")
        return False
    

    # create masked version: replace each entry in each clue-list with "?"
    masked = [ [ ["?" for _ in cl] for cl in part ] for part in orig ]

    def collect_positions(mask):
        pos = []
        for side in (0, 1):
            for li, cl in enumerate(mask[side]):
                for pi, val in enumerate(cl):
                    if val == "?":
                        pos.append((side, li, pi))
        return pos

    steps = []
    # initial solve with all "?"
    top_mask = [list(cl) for cl in masked[0]]
    left_mask = [list(cl) for cl in masked[1]]
    print("Starting initial solve with all clues masked...")
    sol, marked = solve_picross_simple([top_mask, left_mask])
    steps.append({
        "step": 0,
        "changed": None,
        "marked": marked,
        "solution": sol,
    })
    step = 1
    positions = collect_positions(masked)
    print(f"Starting build-up: {marked} cells marked, {len(positions)} clues to reveal.")
    
    solution = None
    with tqdm(total=len(positions)) as pbar:
        while marked < len(clues[0]) * len(clues[1]):
            side, li, pi = choice(positions)
            # install the real value from orig into masked
            value = orig[side][li][pi]
            masked[side][li][pi] = value

            # prepare solver input (deep copy to avoid accidental sharing)
            top_mask = [list(cl) for cl in masked[0]]
            left_mask = [list(cl) for cl in masked[1]]
            
            S = solve_picross_simple([top_mask, left_mask], grid=solution)
            
            if not S:
                print("Error: puzzle became unsolvable after revealing clue", (side, li, pi, value))
                return False
            solution, marked = S
            steps.append({
                "step": step,
                "changed": (side, li, pi, value),
                "marked": marked,
                "solution": copy.deepcopy(solution),
            })
            showSolution(solution)
            step += 1
            positions = collect_positions(masked)
            pbar.update(1)
    return steps, solution

def showSolution(solution):
    print()
    if solution is None:
        print("No solution available")
        return
    for row in solution:
        line = "".join(
            "#" if cell == 1 else
            "." if cell == 3 else
            "?"
            for cell in row
        )
        print(line)
    print()

def create_once(id):
    n = random.choices([5,10,15,20], weights=[0,1,0,0])[0]
    x = n
    y = n

    pars_1 = {
        5: [3, 1.5],
        10: [3, 2],
        15: [4, 3],
        20: [5, 4.2],
    }
    pars_2 = {
        5: 2,
        10: 2.5,
        15: 3,
        20: 4,
    }
    rando_clues, G = generate_random_clues_2(x, y, pars_2[n])
    if not rando_clues:
        return False

    top_clues = rando_clues[0]
    left_clues = rando_clues[1]
    CLUES = [
        top_clues,
        left_clues
    ]

    print(f"Generated {x}x{y} clues, starting build-up...")
    build_up = build_up_game(CLUES)
    if not build_up:
        return False
    
    steps = build_up[0]

    give_away = {}
    number_possible = 0
    
    for info in steps:
        if number_possible not in give_away:
            give_away[number_possible] = []
        give_away[number_possible] += [info["changed"]]
        number_possible = info["marked"]
    if number_possible not in give_away:
        give_away[number_possible] = []
        
    output = {
        "T": top_clues,
        "L": left_clues,
        "S": steps[-1]["solution"],
        "G": give_away
    }
    
    if int(list(output['G'].keys())[-1]) < x * y:
        print("Puzzle not fully solved!!!!!")
        print(output)
        raise Exception("Puzzle not fully solved")
    
        exit()
    
    # make puzzles and spoilers directories if they don't exist
    Path("Site/puzzles").mkdir(exist_ok=True)
    Path("Site/spoilers").mkdir(exist_ok=True)

    with open(f"Site/puzzles/p_{x}_{y}_{len(give_away)}_{id}.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, separators=(',', ':'), ensure_ascii=False)

    with open(f"Site/spoilers/p_{x}_{y}_{len(give_away)}_{id}.txt", "w", encoding="utf-8") as f:
        marked = -1
        for step in steps:
            if step['marked'] != marked:
                f.write(f"# clues: {step['step']:3},  # possible: {step['marked']:3}\n")
                for row in step["solution"]:
                    line = "".join(
                        "#" if cell == 1 else
                        "." if cell == 3 else
                        "?"
                        for cell in row
                    )
                    f.write(line + "\n")
                f.write("\n")
            marked = step['marked']
    return True

# if __name__ == "__main__":
#     random_seed = random.randint(0, 1000000)
#     print("Using random seed:", random_seed)
#     random.seed(random_seed)
    
#     am_puzzles = 0 # don't change ><
    
#     start = 1
#     max_puzzles = 1
    
#     with tqdm(total=max_puzzles) as pbar:
#         while am_puzzles < max_puzzles:
            
#             if create_once(start + am_puzzles + 1):    
#                 am_puzzles += 1
#                 pbar.update(1)
#     make_lists_of_puzzles()

create_once(111111)