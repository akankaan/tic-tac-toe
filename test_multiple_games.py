# Author: AI

import json, ast
import environment as ioppt

def load_v(path):
    raw = json.load(open(path))
    return {tuple(ast.literal_eval(k)): float(v) for k, v in raw.items()}

def board_to_state(b):
    return tuple(b[r][c] for r in range(3) for c in range(3))

def best_move(board, V):
    best_a, best_v = None, float("-inf")
    for a in ioppt.get_empty_positions(board):
        r, c = ioppt.flat_to_board(a)
        nb = [row[:] for row in board]
        nb[r][c] = 1  
        v = V.get(board_to_state(nb), 0.0)
        if v > best_v:
            best_v, best_a = v, a
    return best_a

V = load_v("value_table2.json")
results = {"wins": 0, "draws": 0, "losses": 0}

print("Testing 1000 games...\n")

for test_num in range(1000):
    board = [[0]*3 for _ in range(3)]
    
    while True:
        a = best_move(board, V)
        if a is None:
            results["draws"] += 1
            break
        r, c = ioppt.flat_to_board(a)
        board[r][c] = 1
        
        if ioppt.check_winner(board, 1):
            results["wins"] += 1
            break
        
        opp_a = ioppt.move_decide(board)
        if opp_a == -1:
            results["draws"] += 1
            break
        r, c = ioppt.flat_to_board(opp_a)
        board[r][c] = 2
        
        if ioppt.check_winner(board, 2):
            results["losses"] += 1
            break

print(f"Wins:   {results['wins']}")
print(f"Draws:  {results['draws']}")
print(f"Losses: {results['losses']}")
print(f"\nWin rate: {results['wins']/10}%")
print(f"Draw rate: {results['draws']/10}%")
