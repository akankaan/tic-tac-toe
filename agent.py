# Author: Kaan Akan
# Date  : Feb 7, 2026

import environment as ioppt
import random
import pickle
import json
import itertools

# 0 denotes empty spot, 1 is "X", 2 is "O"
empty_board = [[0, 0, 0], 
               [0, 0, 0],
               [0, 0, 0]]

board = [[0, 0, 0], 
         [0, 0, 0],
         [0, 0, 0]] 

# Generates all board configurations, even if not possible by game rules
all_states = []

all_states = list(itertools.product([0, 1, 2], repeat=9))

# Creates a value table with every value initialized to 0

V = {i: 0.0 for i in all_states}

# Learning parameters
alpha        = 0.2
gamma        = 1.0
episode_num  = 3000000

# epsilon-greedy with exponential decay
initial_epsilon = 1.0
epsilon_decay   = 0.9997

def to_key(b):
    return (
        b[0][0], b[0][1], b[0][2],
        b[1][0], b[1][1], b[1][2],
        b[2][0], b[2][1], b[2][2],
    )

for ep in range(0, episode_num):

    if ( ep % 6000 == 0 ):
        print(( ep * 100 ) / episode_num )
    effective_epsilon = max(0.01, initial_epsilon * (epsilon_decay ** ep))

    board = [[0,0,0],[0,0,0],[0,0,0]]
    done = False

    while not done:
        s = to_key(board)  # X-to-move state

        possible_plays = ioppt.get_empty_positions(board)

        # Choose action based on possible X moves
        if random.random() < effective_epsilon:
            a = random.choice(possible_plays)
        else:
            best_value = -1e9
            best_moves = []

            for move in possible_plays:
                # Makes copy and applies X move to evaluate next state's value (after X move)
                ns_board = [row[:] for row in board]
                r, c = ioppt.flat_to_board(move)
                ns_board[r][c] = 1
                v = V[to_key(ns_board)]

                if v > best_value:
                    best_value = v
                    best_moves = [move]
                elif v == best_value:
                    best_moves.append(move)

            a = random.choice(best_moves)

        # Play X in environment
        board, reward_x, done = ioppt.step_agent(board, a)

        s_after_x = to_key(board)   # After X state (before O moves)

        if done:
            # Terminates right after X
            V[s] = V[s] + alpha * (reward_x - V[s])
            break

        # Environment plays O
        board, reward_o, done = ioppt.step_opponent(board)

        s_after_o = to_key(board)   # After O state (before X moves the next round)

        # Update state after x had played
        if done:
            # If game terminates after O moves, s_after_x should go to -1
            V[s_after_x] = V[s_after_x] + alpha * (reward_o - V[s_after_x])
        else:
            V[s_after_x] = V[s_after_x] + alpha * ((reward_o + gamma * V[s_after_o]) - V[s_after_x])

        # Updates state before X had moved
        V[s] = V[s] + alpha * ((reward_x + gamma * V[s_after_x]) - V[s])


# Save value table with pickle        
# with open("value_table.pkl", "wb") as f:
#     pickle.dump(V, f)

V = dict(list(V.items()))

# Save value table with json
with open("value_table2.json", "w") as f:
    json.dump({str(k): v for k, v in V.items()}, f)     

