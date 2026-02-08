# Author: Kaan Akan
# Date  : Feb 4, 2026 

# A tic-tac-toe player with the following heuristic: 
# 1) If opponent can win in one move, prevent the move
# 2) If you can win in one move, make the move
# 3) Otherwise, play a random move

# Hint: If you capture two corner pieces and then the center piece,
#       you have a high chance of winning

import random

"""
Board position index numbering representation:

[[0, 1, 2], 
 [3, 4, 5],
 [6, 7, 8]]

"""

WINNING_POS = [[0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
               [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
               [0, 4, 8], [2, 4, 6]]             # diagonals

# Converts board coordinates to numbers from 0 to 8
def board_to_flat(row, col):
    return row * 3 + col

# Converts number index back to board coordinates
def flat_to_board(flat_index):
    return flat_index // 3, flat_index % 3

# Returns a list with the indexes of empty board positions
def get_empty_positions(board):

    empty = []
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == 0:
                empty.append(board_to_flat(i, j)) # Get index of empty coordinate
    return empty

# Checks to see if there is a winner after move has been played
def check_winner(board, player):

    for i in range(0, len(WINNING_POS)):
        winning_combo = WINNING_POS[i]

        match_found = True

        # Searches through each winning combination
        for j in range(0, len(winning_combo)):
            index = winning_combo[j]
            row, col = flat_to_board(index) # Gets coordinate of positions in comb

            if board[row][col] != player:
                match_found = False
                break
        
        if match_found:
            return True
        
    return False
        
# Checks if either player can win in one move
def can_win_in_one_move(board, player):

    empty_positions = get_empty_positions(board)
    
    for i in range(0, len(empty_positions)):
        row, col = flat_to_board(empty_positions[i])

        # Try placing player's piece
        board[row][col] = player
        
        if (check_winner(board, player)):
            board[row][col] = 0  # Undo
            return empty_positions[i]
        
        board[row][col] = 0  # Undo
    
    return -1

# Computer decides its move based on the   
# heuristic detailed at the top of this file
def move_decide(board):

    # Check if computer (player 2) can win
    winning_move = can_win_in_one_move(board, 2)
    if ( winning_move != -1 ):
        return winning_move
    
    # Check if opponent (player 1) can win so can be blocked
    blocking_move = can_win_in_one_move(board, 1)
    if ( blocking_move != -1 ):
        return blocking_move
    
    # Otherwise pick random move
    empty_positions = get_empty_positions(board)
    if empty_positions:
        move = random.choice(empty_positions)
        return move
    
    return -1

def play_turn(board, player_move):

    empty_positions = get_empty_positions(board)
    if player_move not in empty_positions:
        return board, 0, True  # give 0 to reinforce illegal moves are bad

    # player move (X)
    r, c = flat_to_board(player_move)
    board[r][c] = 1
    if check_winner(board, 1):
        return board, +1, True
    if len(get_empty_positions(board)) == 0:
        return board, 0.55, True  # i think drawing should be more good than bad
                           # for my purposes so made it closer to 1

    # opponent move (O)
    opp_move = move_decide(board)
    r, c = flat_to_board(opp_move)
    board[r][c] = 2
    if check_winner(board, 2):
        return board, 0, True
    if len(get_empty_positions(board)) == 0:
        return board, 0, True  # draw

    return board, 0, False
