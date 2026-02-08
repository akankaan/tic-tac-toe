# Author: Kaan Akan
# Date  : Feb 7, 2026

import imperfect_opponent_for_training as ioppt

# 0 denotes empty spot, 1 is "X", 2 is "O"
empty_board = [[0, 0, 0], 
               [0, 0, 0],
               [0, 0, 0]]

board = [[0, 0, 0], 
         [0, 0, 0],
         [0, 0, 0]] 

done = 0
while not done:

    val = int(input("enter: "))
    next_state, reward, done = ioppt.play_turn(board,val)
    print(next_state, reward, done)
