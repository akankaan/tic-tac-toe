# Author: AI

import ast
import json
import random
import environment as ioppt

AGENT = 1   # X
HUMAN = 2   # O

def to_key(b):
    return (
        b[0][0], b[0][1], b[0][2],
        b[1][0], b[1][1], b[1][2],
        b[2][0], b[2][1], b[2][2],
    )

def print_board(b):
    # show 0/1/2 as . / X / O for readability
    sym = {0: ".", 1: "X", 2: "O"}
    for r in range(3):
        print(" ".join(sym[b[r][c]] for c in range(3)))
    print()

def load_value_table(path="value_table2.json"):
    # Your file saves keys as strings like "(0, 1, 0, ...)"
    with open(path, "r") as f:
        raw = json.load(f)
    V = {ast.literal_eval(k): float(v) for k, v in raw.items()}
    return V

def agent_choose_move(board, V, epsilon=0.0):
    possible = ioppt.get_empty_positions(board)
    if not possible:
        return -1

    # epsilon-greedy (set epsilon=0 for pure greedy play)
    if random.random() < epsilon:
        return random.choice(possible)

    best_val = -1e18
    best_moves = []

    for move in possible:
        ns = [row[:] for row in board]
        r, c = ioppt.flat_to_board(move)
        ns[r][c] = AGENT  # X plays
        v = V.get(to_key(ns), 0.0)  # default 0 if missing

        if v > best_val:
            best_val = v
            best_moves = [move]
        elif v == best_val:
            best_moves.append(move)

    return random.choice(best_moves)

def human_move(board):
    possible = set(ioppt.get_empty_positions(board))
    while True:
        try:
            mv = int(input("Your move (0..8): ").strip())
        except ValueError:
            print("Please enter an integer 0..8.")
            continue
        if mv in possible:
            return mv
        print(f"Illegal. Empty positions: {sorted(possible)}")

def main():
    V = load_value_table("value_table2.json")
    board = [[0,0,0],[0,0,0],[0,0,0]]
    done = False

    print("You are O=2. Agent is X=1. Enter moves as 0..8 (row-major).")
    print_board(board)

    while not done:
        # ----- Agent (X) plays -----
        a = agent_choose_move(board, V, epsilon=0.0)
        board, reward_x, done = ioppt.step_agent(board, a)
        print(f"Agent played: {a} reward: {reward_x} done: {done}")
        print_board(board)
        if done:
            break

        # ----- Human (O) plays -----
        mv = human_move(board)

        # Apply human move using environment's helpers (no new env functions)
        r, c = ioppt.flat_to_board(mv)
        board[r][c] = HUMAN

        # Check terminal after human move (reuse env check_winner)
        if ioppt.check_winner(board, HUMAN):
            print("You (O) win!")
            done = True
        elif len(ioppt.get_empty_positions(board)) == 0:
            print("Draw.")
            done = True

        print_board(board)

    # Print final result from agent perspective if desired
    if ioppt.check_winner(board, AGENT):
        print("Agent (X) wins!")
    elif ioppt.check_winner(board, HUMAN):
        print("Final: You (O) win.")
    else:
        print("Final: Draw.")

if __name__ == "__main__":
    main()
