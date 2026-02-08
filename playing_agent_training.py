# Author: Kaan Akan
# Date  : Feb 7, 2026

import imperfect_opponent_for_training as ioppt
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

alpha        = 0.1
gamma        = 1 # so not used in eq
episode_num  = 100000
explore_rate = 0.1 # between 0-1

for ep in range(0, episode_num):

    # Reset board and done before each episode

    board = [[0,0,0],[0,0,0],[0,0,0]]
    done = False

    while not done:

        possible_plays = ioppt.get_empty_positions(board)

        # Generates next state options from possible moves

        possible_next_states = []
        for i in range(0, len(possible_plays)):
            possible_next_state = []

            # Copy unchanged board to possible next state
            for j in range(0, len(board)):
                new_row = []

                for k in range(0, len(board[0])):
                    new_row.append(board[j][k])
                possible_next_state.append(new_row)
            
            row, col = ioppt.flat_to_board(possible_plays[i])
            possible_next_state[row][col] = 1
            possible_next_states.append(possible_next_state)
        
        # Searches next states from the value function 
        # to find the best move

        best_value = -10
        best_moves = []

        for i in range(0, len(possible_next_states)):
            ns = possible_next_states[i]
            key = (
                ns[0][0], ns[0][1], ns[0][2],
                ns[1][0], ns[1][1], ns[1][2],
                ns[2][0], ns[2][1], ns[2][2],
            )

            val = V[key]

            if val > best_value:
                best_value = val
                best_moves = [possible_plays[i]]
            elif val == best_value:
                best_moves.append(possible_plays[i])

        best_move = random.choice(best_moves)

        s_before = (
                        board[0][0], board[0][1], board[0][2],
                        board[1][0], board[1][1], board[1][2],
                        board[2][0], board[2][1], board[2][2],
                    )
        
        # Add explaratory move 

        if ( random.random() < explore_rate ): 
            best_move = random.choice(possible_plays) 
        
        # Play with found best move for X only

        board, reward, done = ioppt.step_agent(board, best_move)

        s_after =  (
                    board[0][0], board[0][1], board[0][2],
                    board[1][0], board[1][1], board[1][2],
                    board[2][0], board[2][1], board[2][2],
                    )

        # Update after agent step:
        # V(s) <- V(s) + ⍺(R + V(s') - V(s))

        if done:    
            V[s_before] = V[s_before] + alpha * (reward             - V[s_before])
        else:
            V[s_before] = V[s_before] + alpha * (reward + V[s_after] - V[s_before])

        if done:
            break

        # Opponent plays O only

        s_before_opp = s_after

        board, reward, done = ioppt.step_opponent(board)

        s_after =  (
                    board[0][0], board[0][1], board[0][2],
                    board[1][0], board[1][1], board[1][2],
                    board[2][0], board[2][1], board[2][2],
                    )

        # Update after opponent step (environment transition from s_before_opp):

        V[s_before_opp] = V[s_before_opp] + alpha * (reward + V[s_after] - V[s_before_opp])

# Save value table with pickle        
# with open("value_table.pkl", "wb") as f:
#     pickle.dump(V, f)

V_1000 = dict(list(V.items())[:1000])

# Save value table with json
with open("value_table2.json", "w") as f:
    json.dump({str(k): v for k, v in V_1000.items()}, f)     

