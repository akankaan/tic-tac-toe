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

# Test a full game
V = load_v("value_table2.json")
board = [[0]*3 for _ in range(3)]

print("=== Testing Agent Performance ===\n")

for turn in range(5):
    a = best_move(board, V)
    if a is None:
        break
    r, c = ioppt.flat_to_board(a)
    board[r][c] = 1
    print(f"Agent move {turn+1}: position {a}")
    print(board[0])
    print(board[1])
    print(board[2])
    print()
    
    if ioppt.check_winner(board, 1):
        print("✓ Agent won!")
        break
    
    opp_a = ioppt.move_decide(board)
    if opp_a == -1:
        print("Draw!")
        break
    r, c = ioppt.flat_to_board(opp_a)
    board[r][c] = 2
    print(f"Opponent move: position {opp_a}")
    print(board[0])
    print(board[1])
    print(board[2])
    print()
    
    if ioppt.check_winner(board, 2):
        print("✗ Opponent won!")
        break
