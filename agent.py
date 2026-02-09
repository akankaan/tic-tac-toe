# Author: Kaan Akan
# Date  : Feb 7, 2026

import environment as ioppt
import random
import pickle
import json

# 0 denotes empty spot, 1 is "X", 2 is "O"
empty_board = [[0, 0, 0], 
               [0, 0, 0],
               [0, 0, 0]]

board = [[0, 0, 0], 
         [0, 0, 0],
         [0, 0, 0]] 

# Generates all board configurations, even if not possible by game rules
all_states = []

def state_generation():
    for a in range(0, 3):
        for b in range(0, 3):
            for c in range(0, 3):
                for d in range(0, 3):
                    for e in range(0, 3):
                        for f in range(0, 3):
                            for g in range(0, 3):
                                for h in range(0, 3):
                                    for i in range(0, 3):
                                        all_states.append([[a, b, c], 
                                                           [d, e, f],
                                                           [g, h, i]])

state_generation()

# Creates a value table with every value initialized to 0
V = {}

for i in all_states:
    key = (
        i[0][0], i[0][1], i[0][2],
        i[1][0], i[1][1], i[1][2],
        i[2][0], i[2][1], i[2][2],
    )
    V[key] = 0

# Learning parameters
alpha        = 0.2
gamma        = 1.0
episode_num  = 300000

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

        if done:
            # Check termination right after X move
            V[s] = V[s] + alpha * (reward_x - V[s])
            break

        # Environment plays O
        board, reward_o, done = ioppt.step_opponent(board)

        tot_reward = reward_x + reward_o

        if done:
            # Finishes after O moves
            V[s] = V[s] + alpha * (tot_reward - V[s])
        else:
            s_next = to_key(board)  # next X-to-move state
            V[s] = V[s] + alpha * ((tot_reward + gamma * V[s_next]) - V[s])

# Save value table with pickle        
# with open("value_table.pkl", "wb") as f:
#     pickle.dump(V, f)

V = dict(list(V.items()))

# Save value table with json
with open("value_table2.json", "w") as f:
    json.dump({str(k): v for k, v in V.items()}, f)     

