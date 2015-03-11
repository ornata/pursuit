import sys
import networkx as nx
#import matplotlib.pyplot as plt
import read_graph as rg

SHOW_MAT = False
SHOW_STRATEGY = True
PLAY_GAME = False

'''
Formatted printing for relation matrix
'''
def print_rel_mat(mat):

    for row in mat:
        for column in row:
            print " ",
            if column[0] == sys.maxint:
                print "-",
            else:
                print column,
            print " ",
        print ""

'''
Formatted printing for strategies
'''
def print_strategy(strategy):
    for row in strategy:
        for x in row:
            print " ",
            if x == sys.maxint:
                print "inf",
            else:
                print x,
        print ""

def find_legal_moves(allowed_moves, current_pos):
    legal = []
    for x in allowed_moves:
        if x[0] == current_pos:
            legal.append(x[1])
    return legal

'''
Checks if there are any values that we can update during the process.
Returns true if something was changed, false otherwise.

We can update something if given the current information, for any move
right could possibly make, there is some move that left can make to get
closer to winning.
'''
def change_entry(rel_mat, r, l, allowed_left, allowed_right):

    # The current positions have already been labelled.
    if (rel_mat[r][l])[0] != sys.maxint:
        return False

    # Otherwise, check if we can label something.
    nbrs_r = find_legal_moves(allowed_left, r)
    nbrs_l = find_legal_moves(allowed_right, l)

    countermoves = [0]*len(nbrs_r) # used as a counter

    i = 0 # used to index countermoves
    label = 0
    prev_label = sys.maxint # assume unlabelled position

    for rpos in nbrs_r:
        for lpos in nbrs_r:
            # can we find an lpos that counters rpos?
            if (rel_mat[lpos][rpos])[0] < (rel_mat[r][l])[0]:
                if prev_label > label + 1:
                    label = rel_mat[lpos][rpos][0] + 1
                    prev_label = label
                countermoves[i] = 1
                break
        i = i + 1

    if(all(v==1 for v in countermoves)):
        rel_mat[r][l] = [label, (r, l)]
        return True
    
    else:
        return False


'''
Call change entry for every possible position until
nothing can be updated.
'''
def update_matrix(right, left, rel_mat, allowed_left, allowed_right):
    no_update = True

    for i in range(0, len(left)):
        for j in range(0, len(right)):
            c = change_entry(rel_mat, j, i, allowed_left, allowed_right) 
            if c == True:
                # Show current state of game
                if(SHOW_MAT == True):
                    print "Relation matrix"
                    print_rel_mat(rel_mat)
                    print ""

                no_update = False

    return no_update


'''
Attempt to fill the relation matrix up.
If we can remove all instances of sys.maxint, then left wins.
Otherwise, right wins.
'''
def fill_matrix(left, right, rel_mat, allowed_left, allowed_right):

    done = False

    while done == False:
        done = update_matrix(right, left, rel_mat, allowed_left, allowed_right)

    # Check if there are any rows we didn't manage
    # to relabel.
    for row in rel_mat:
        for i in row:
            if sys.maxint in i:
                return "Right"

    # There are no unlabelled rows.
    return "Left"


'''
Generate the strategy that left will follow if we play the game.
This is all of the values from the relation matrix with rows
representing the position of left and columns representing the
position of right.
'''
def gen_left_strategy(rel_mat):
    k = len(rel_mat)
    m = len(rel_mat[0])

    strategy = [[sys.maxint for j in range(m)] for i in range(k)]

    minimum = sys.maxint #this is the minimum move found so far

    for row in range(k):
        for col in range(m):
            strategy[row][col] = rel_mat[row][col][0]

    if SHOW_STRATEGY == True:
        print "Left's strategy"
        print_strategy(strategy)
    return strategy


'''
If the winner is right, generate a matrix containing right's winning
strategy.

Rows: position of left
Cols: position of right

Any move that would cause right to lose is labelled -1.
Otherwise, put in the value from the relation matrix.

Rows are left's position, columns are rights position.
'''
def gen_right_strategy(rel_mat):
    k = len(rel_mat)
    m = len(rel_mat[0])

    strategy = [[-1 for j in range(m)] for i in range(k)]

    for row in range(k):
        for col in range(m):
            # any move with a value of 0 would make right lose
            if(rel_mat[row][col][0] > 0):
                strategy[row][col] = rel_mat[row][col][0]

    if SHOW_STRATEGY == True:
        print "Right's strategy"
        print_strategy(strategy)

    return strategy


'''
Play the game to find the winning strategy for left/right
Left moves first, then right moves.
'''
def play_game(left_strategy, right_strategy, start_left, start_right, allowed_left, allowed_right):
    left = start_left
    right = start_right
    nmoves = -1

    print "\n Play the game \n"
    print "Starting position:"

    nmoves = left_strategy[left][right]

    print (left,right)

    print "Left's allowed moves"
    print allowed_left

    print "Right's allowed moves"
    print allowed_right

    while True:
        if nmoves == sys.maxint or nmoves == 0:
            break

        best_move = left

        for move in allowed_left:
            if move[0] == left and left_strategy[move[1]][right] < left_strategy[best_move][right]:
                    best_move = move[1]

        left = best_move

        nmoves = left_strategy[left][right]

        print "Left moves to %d" %(left)
        print (left,right)
        print "Number of moves until left can win: %d" %(nmoves)
        print ""

        if nmoves == sys.maxint or nmoves == 0:
            break

        best_move = right

        for move in allowed_right:
            if move[0] == right and right_strategy[left][move[1]] > right_strategy[left][best_move]:
                    best_move = move[1]
        
        right = best_move
        nmoves = right_strategy[left][right]

        print "Right moves to %d" %(right)
        print (left,right)
        print "Number of moves until left can win: %d" %(nmoves)
        print ""


'''
Read in the graphs, allowed states, start states, and final states.
Construct the game matrix from the graphs and initialize with the
start states of the graph.
Print a winning message after running the game.
'''
def main():

    game = rg.read_game()

    left = game[0]
    right = game[1]
    allowed_left = game[2]
    allowed_right = game[3]
    final_states = game[4]
    start_left = game[5]
    start_right = game[6]

    # Game info stored like [number of moves until win, (left_position, right_position)]
    relation_matrix = [[[sys.maxint, (i, j)] for j in range(0, len(right))] for i in range(0, len(left))]

    # Initialize the relation matrix.
    for state in final_states:
        l_pos = state[0]
        r_pos = state[1]
        (relation_matrix[l_pos][r_pos])[0] = 0

    #Run the game, record the winner.
    winner = fill_matrix(left, right, relation_matrix, allowed_left, allowed_right)
    print "\nWinner: %s \n" %(winner)

    left_strategy = gen_left_strategy(relation_matrix)
    right_strategy = gen_right_strategy(relation_matrix)

    if PLAY_GAME == True:
        play_game(left_strategy, right_strategy, start_left, start_right, allowed_left, allowed_right)


if __name__ == "__main__":
    main()
