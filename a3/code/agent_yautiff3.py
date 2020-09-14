"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cached_states = {}
start = time.time()

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    (num_dark,num_light) = get_score(board)
    if color == 1: # dark
        return num_dark - num_light
    if color == 2: # light
        return num_light - num_dark

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return compute_utility(board,color) #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #IMPLEMENT
    opp_color = 3-color
    
    if (limit == 0) or (time.time()-start >= 9.9): # depth limit reached
        return (None,compute_heuristic(board,color))
    
    legal_moves = get_possible_moves(board,opp_color)
    if len(legal_moves) == 0: 
        # if we are at a terminal state, just return the utility
        # there is no further move to select
        return (None,compute_utility(board,color))
    
    # we want to minimize what the max player can accomplish next
    # first get the maximum utility for the next player (which should be 2) for all states
    min_util = float('inf')
    best_move = None
    for move in legal_moves:
        # get the board state for each potential next move
        succ_board = play_move(board,opp_color,move[0],move[1])
        
        (next_move,utility) = minimax_max_node(succ_board,color,limit-1,caching)    
        if utility < min_util:
            min_util = utility
            best_move = move
    
    return (best_move,min_util)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT
    if (limit == 0) or (time.time()-start >= 9.9): # depth limit reached
        return (None,compute_heuristic(board,color))
    
    legal_moves = get_possible_moves(board,color)
    if len(legal_moves) == 0: 
        # if we are at a terminal state, just return the utility
        # there is no further move to select
        return (None,compute_utility(board,color))
    
    # we want to minimize what the max player can accomplish next
    # first get the maximum utility for the next player (which should be 2) for all states
    max_util = -float('inf')
    best_move = None
    for move in legal_moves:
        # get the board state for each potential next move
        succ_board = play_move(board,color,move[0],move[1])
        
        (next_move,utility) = minimax_min_node(succ_board,color,limit-1,caching)    
        if utility > max_util: # max node wants to maximize the minimum utility
            max_util = utility
            best_move = move
    
    return (best_move,max_util)    

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT
    global start 
    start = time.time()
    if board in cached_states:
        state = cached_states[board]
        if state[2] == color:
            (move,utility) = state[0:2]
            return move
    (move,utility) = minimax_max_node(board,color,limit,caching) # max node
    if (caching):
        cached_states[board] = (move,utility,color)
    return move


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    opp_color = 3-color

    if (limit == 0) or (time.time()-start >= 9.9): # depth limit reached
        return (None,compute_heuristic(board,color))
    
    legal_moves = get_possible_moves(board, opp_color)
    # if reached terminal state
    if len(legal_moves) == 0 or limit == 0:
        return (None, compute_utility(board, color))
    best_move = None
    sorted_moves = []
    # find utility of all legal moves
    for move in legal_moves:
        succ_board = play_move(board, opp_color, move[0], move[1])
        sorted_moves.append((move, succ_board))
    # Sort the list by utility
    if (ordering):
        sorted_moves.sort(key = lambda util: compute_utility(util[1], color))
    for move in sorted_moves:
        (next_move, utility) = alphabeta_max_node(move[1], color, alpha, beta, limit-1)
        if utility < beta:
            beta = utility
            best_move = move[0]
        if beta <= alpha:
            return best_move, beta
    return best_move, beta



def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    if (limit == 0) or (time.time()-start >= 9.9): # depth limit reached
        return (None,compute_heuristic(board,color))
    
    legal_moves = get_possible_moves(board, color)
    # if reached terminal state
    if len(legal_moves) == 0 or limit == 0:
        return (None, compute_utility(board, color))
    best_move = None
    sorted_moves = []
    # find utility of all legal moves
    for move in legal_moves:
        succ_board = play_move(board, color, move[0], move[1])
        sorted_moves.append((move, succ_board))
    # Sort list in descending order by utility
    if (ordering):
        sorted_moves.sort(key = lambda util: compute_utility(util[1], color), reverse=True)
    for move in sorted_moves:
        (next_move, utility) = alphabeta_min_node(move[1], color, alpha, beta, limit-1)        
        if utility > alpha: 
            alpha = utility
            best_move = move[0]
        if alpha >= beta:
            return best_move, alpha
    return best_move, alpha

    

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT
    global start 
    start = time.time()
    # initialize alpha and beta
    alpha = -float('inf')
    beta = float('inf')
    if board in cached_states:
        state = cached_states[board]
        if state[2] == color:
            (move,utility) = state[0:2]
            return move
    (move,utility) = alphabeta_max_node(board, color, alpha, beta, limit) # max node
    if (caching):
        cached_states[board] = (move,utility,color)
    return move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
