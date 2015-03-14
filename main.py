import sys
import networkx as nx
#import matplotlib.pyplot as plt
import read_graph as rg

SHOW_MAT = False
SHOW_STRATEGY = True
PLAY_GAME = False

'''
print_rel_mat
-----------------------------------------------------------------------------
Formatted printing for relation matrix
'''
def print_rel_mat(mat):

    for row in mat:
        for column in row:
            print " ",
            if column[0] == sys.maxint:
                print "----------",
            else:
                print column,
            print " ",
        print ""

'''
print_strategy
-----------------------------------------------------------------------------
Formatted printing for strategies
'''
def print_strategy(strategy):
    for row in strategy:
        for x in row:
            print " ",
            if x == sys.maxint:
                print "inf",
            else:
                print "%3d" %(x),
        print ""

'''
find_legal_moves
-----------------------------------------------------------------------------
Returns a list of all of the positions current_pos can move to given a list of tuples (x,y).
If x = current_pos, then append y to the list.
'''
def find_legal_moves(allowed_moves, current_pos):
    legal = []
    for x in allowed_moves:
        if x[0] == current_pos:
            legal.append(x[1])
    return legal

'''
relabel
-----------------------------------------------------------------------------
Check if there is a way for the left player to get closer to winning the game
given any of the moves the right player could make from its current position.

Given the current position (left, right)
For any legal move the right player could make, check if there is a left move
that has a smaller label than (left,right) in the relation matrix.If there is,
then left can walk through that spot in one step, so it may be possible for it
to shorten the game. If it is possible to do that for every single move the right
player can make, then no matter what, left can do better so we can update its label.
We choose the smallest possible label out of each "better" play left could make.

If it is not possible for left to shorten the game no matter what right does, we
can't say anything about a guaranteed better strategy and so we can't update anything.

Returns True if the position (left, right) was relabeled, False otherwise.
'''
def relabel(rel_mat, l, r, allowed_left, allowed_right):

    # The current positions have already been labelled, so nothing can be updated.
    if (rel_mat[l][r])[0] != sys.maxint:
        return False

    # Otherwise, look at all of the legal moves for left and right
    nbrs_r = find_legal_moves(allowed_right, r)
    nbrs_l = find_legal_moves(allowed_left, l)

    # Set the i-th entry to true only if there is a move left can make to shorten the game.
    was_countered = [False]*len(nbrs_r)
    i = 0

    label = rel_mat[l][r][0]
    prev_label = sys.maxint
    candidate_labels = [] # Candidates for relabeling

    # Try to update the current position using its neighbours.
    for rmove in nbrs_r:
        for lmove in nbrs_l:
            move_label = rel_mat[lmove][rmove][0]
            if move_label < label: # We were able to reach this state in fewer moves than the current one
                candidate_labels.append(move_label+1)
                was_countered[i] = True
                break
        i += 1

    if(all(move == True for move in was_countered)):
        rel_mat[l][r] = [min(candidate_labels), (l, r)]
        return True
    
    else:
        return False


'''
update_matrix
-----------------------------------------------------------------------------
Call change entry for every possible position until nothing can be updated.
Once nothing can be updated, it isn't possible for Left to shorten the game
so we are done.

Returns True when nothing was updated at this step, and False otherwise.
'''
def update_matrix(right, left, rel_mat, allowed_left, allowed_right):

    done = True

    for i in range(0, len(left)):
        for j in range(0, len(right)):
            updated_entry = relabel(rel_mat, i, j, allowed_left, allowed_right) 
            if updated_entry == True:
                # Show current state of game
                if(SHOW_MAT == True):
                    print "Updated an entry"
                    print_rel_mat(rel_mat)
                    print ""

                done = False
    return done


'''
fill_matrix
-----------------------------------------------------------------------------
Calls update_matrix until it returns done = True. At this point, nothing
was updated so the game is over. After, it checks whether or not
the relation matrix was filled up. If it wasn't, then Right won. Otherwise,
left won.

Returns a string stating the winner of the game.
'''
def fill_matrix(left, right, rel_mat, allowed_left, allowed_right):

    done = False
    while done == False:
        done = update_matrix(right, left, rel_mat, allowed_left, allowed_right)

    for row in rel_mat:
        for i in row:
            # We failed to fill the matrix so right wins
            if sys.maxint in i:
                return "Right"

    # There are no unlabelled rows.
    return "Left"


'''
gen_left_strategy
-----------------------------------------------------------------------------
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
gen_right_strategy
-----------------------------------------------------------------------------
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
play_game
-----------------------------------------------------------------------------
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
init_relation_matrix
-----------------------------------------------------------------------------
Initialize the relation matrix for the game and return it.
'''
def init_relation_matrix(left, right, final_states):
    # Game info stored like [number of moves until win, (left_position, right_position)]
    relation_matrix = [[[sys.maxint, (i, j)] for j in range(0, right)] for i in range(0, left)]

    # Initialize the relation matrix.
    for state in final_states:
        l_pos = state[0]
        r_pos = state[1]
        (relation_matrix[l_pos][r_pos])[0] = 0
    return relation_matrix

'''
main
-----------------------------------------------------------------------------
Read in the graphs, allowed states, start states, and final states.
Construct the game matrix from the graphs and initialize with the
start states of the graph.
Print a winning message after running the game.
'''
def main():

    while True:
        game = rg.read_game()

        if game == None:
            break

        left = game[0]
        right = game[1]
        allowed_left = game[2]
        allowed_right = game[3]
        final_states = game[4]
        start_left = game[5]
        start_right = game[6]

        relation_matrix = init_relation_matrix(len(left), len(right), final_states)

        # Run the game, record the winner.
        winner = fill_matrix(left, right, relation_matrix, allowed_left, allowed_right)
        print "\nWinner: %s \n" %(winner)

        # Find the strategies that left and right will try and follow to win the game
        left_strategy = gen_left_strategy(relation_matrix)
        right_strategy = gen_right_strategy(relation_matrix)

        # If the flag is set, show how left (or right) would win the game given start_left and start_right
        if PLAY_GAME == True:
            play_game(left_strategy, right_strategy, start_left, start_right, allowed_left, allowed_right)

        game = []


if __name__ == "__main__":
    main()
