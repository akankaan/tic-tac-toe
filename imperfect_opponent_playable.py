# Author: Kaan Akan
# Date  : Feb 4, 2026 

# A tic-tac-toe player with the following heuristic: 
# 1) If opponent can win in one move, prevent the move
# 2) If you can win in one move, make the move
# 3) Otherwise, play a random move

# Hint: If you capture two corner pieces and then the center piece,
#       you have a high chance of winning

import random

# 0 denotes empty spot, 1 is "X", 2 is "O"
empty_board = [[0, 0, 0], 
               [0, 0, 0],
               [0, 0, 0]]

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

# Prints board in a flat format
def print_board(board):
    print(" 0 1 2")
    for i in range(0, 3):
        row_str = str(i) + " "
        for j in range(0, 3):
            piece = board[i][j]
            if piece == 0:
                row_str = row_str + ". "
            elif piece == 1:
                row_str = row_str + "X "
            elif piece == 2:
                row_str = row_str + "O "
        print(row_str)
    print(" ")

# Computer decides its move based on the   
# heuristic detailed at the top of this file
def move_decide(board):

    # Check if computer (player 2) can win
    winning_move = can_win_in_one_move(board, 2)
    if ( winning_move != -1 ):
        print("Computer plays winning move at position " + str(winning_move))
        return winning_move
    
    # Check if opponent (player 1) can win so can be blocked
    blocking_move = can_win_in_one_move(board, 1)
    if ( blocking_move != -1 ):
        print("Computer blocks opponent at position " + str(blocking_move))
        return blocking_move
    
    # Otherwise pick random move
    empty_positions = get_empty_positions(board)
    if empty_positions:
        move = random.choice(empty_positions)
        print("Computer plays random move at position " + str(move))
        return move
    
    return -1

def play_game():

    board = []
    
    for i in range(0, len(empty_board)):
        new_row = []

        for j in range(0, len(empty_board[0])):
            new_row.append(empty_board[i][j])
        board.append(new_row)

    print("------------")
    print("Welcome to Tic-Tac-Toe!")
    print("You are X, Computer is O")
    print("Positions are numbered 0-8:")
    print_board(empty_board)
    print("------------")
    
    continue_loop = 1

    while ( continue_loop == 1 ):

        print("Current board:")
        print_board(board)
        
        # Check if game is over
        if check_winner(board, 1):
            print("You won!")
            break
        if check_winner(board, 2):
            print("Computer won!")
            break
        
        empty_positions = get_empty_positions(board)
        if ( len(empty_positions) == 0 ):
            print("It's a draw!")
            break
        
        # Player's move

        valid_move = False
        while not valid_move:
            try:
                player_move = int(input("Enter your move (0-8): "))
                if player_move not in empty_positions:
                    print("Invalid move. Position isn't empty or out of range")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
                continue
        
        row, col = flat_to_board(player_move)
        board[row][col] = 1
        
        # Check if player won
        if check_winner(board, 1):
            print("Current board:")
            print_board(board)
            print("You won!")
            break
        
        # Computer move
        computer_move = move_decide(board)
        if ( computer_move == -1 ):
            print("It's a draw!")
            break
        
        row, col = flat_to_board(computer_move)
        board[row][col] = 2

if __name__ == "__main__":
    play_game()