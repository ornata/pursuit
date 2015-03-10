import sys
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import re


## Formatted printing for relation matrix
def pmat(mat):

    for row in mat:
        for column in row:
            print " ",
            if column[0] == sys.maxint:
                print "-",
            else:
                print column,
            print " ",

        print ""


## Checks if there are any values that we can update during the process.
## Returns true if something was changed, false otherwise.
def corner(rel_mat, curr_j, curr_i, right, left):

    # If we aren't finding anything new, there's nothing to update.
    if (rel_mat[curr_i][curr_j])[0] != sys.maxint:
        return False

    nbrs_i = left.neighbors(curr_i)
    nbrs_j = right.neighbors(curr_j)

    li = [0]*right.out_degree(curr_j) # acts as a counter

    count = 0 # used to index li
    rel_val = 0
    prev_rel_val = sys.maxint

    for right_vert in nbrs_j:
        for left_vert in nbrs_i:

            if (rel_mat[left_vert][right_vert])[0] < (rel_mat[curr_i][curr_j])[0]:
                if prev_rel_val > rel_val + 1:
                    rel_val = rel_mat[left_vert][right_vert][0] + 1
                    prev_rel_val = rel_val
                li[count] = 1
                break
        count = count + 1

    if(all(v==1 for v in li)):

        rel_mat[curr_i][curr_j] = [rel_val, (curr_i, curr_j)]
        return True
    
    else:
        return False


## Check if any values in the matrix can be updated.
def iterate_matrix(right, left, rel_mat):
    done = True

    for i in range(0, len(left)):
        for j in range(0, len(right)):
            c = corner(rel_mat, j, i, right, left)
            if c == True:
                print "Relation matrix"
                pmat(rel_mat)
                print ""
                #time.sleep(1)
                done = False

    return done


## Run the game until the matrix is full, if possible.
def run_game(left, right, rel_mat):

    done = False

    while done == False:
        done = iterate_matrix(right, left, rel_mat)

    for row in rel_mat:
        for i in row:
        # There is an unlabelled row.
            if sys.maxint in i:
                return "Right"

    # There are no unlabelled rows.
    return "Left"


## If the winner is left, generate a matrix containing left's winning
## strategy.
## Input: - The relation matrix from the game
## M: Populate the matrix so that each cell contains the
##                minimum number of moves that it would take to win
##                the game.
## Columns: Right's position
## Rows: Left's position
def gen_left_strategy(rel_mat):
    k = len(rel_mat)
    m = len(rel_mat[0])

    strategy = [[sys.maxint for j in range(m)] for i in range(k)]

    minimum = sys.maxint #this is the minimum move found so far

    # for each of left's possible positions
    # choose the position that right is in such that it is the smallest

    for row in range(k):
        for col in range(m):
            strategy[row][col] = rel_mat[row][col][0]

    print "=== Left's strategy ==="
    for row in strategy:
        print row

    return strategy

## Play the game to find the winning strategy for left/right
## Left moves first, then right moves.
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



## If the winner is right, generate a matrix containing right's winning
## strategy.
## Matrix format: Any move that would cause right to lose, put in a dummy
##                Any move that allows right to prolong the game, put in
##                the number of moves from the game matrix.
## Columns: Right's position
## Rows: Left's position
def gen_right_strategy(rel_mat):
    k = len(rel_mat)
    m = len(rel_mat[0])
    strategy = [[-1 for j in range(m)] for i in range(k)]

    for row in range(k):
        for col in range(m):
            if(rel_mat[row][col][0] > 0):
                strategy[row][col] = rel_mat[row][col][0]

    print "=== Right's strategy ==="
    for row in strategy:
        print row
    return strategy

def read_graph(n, number):
    G = nx.DiGraph()

    G.add_nodes_from([x for x in range(0,n)])

    nodes_read = 0 

    while nodes_read < n:
        source = read_digit(number)
        target = read_line(number)
        edges = [(source,y) for y in target]
        G.add_edges_from(edges)
        nodes_read +=1

    return G

def read_line(number):
    line = []
    ch = " "
    while ch != "\n" and ch != "":
        ch = sys.stdin.read(1)
        if(re.match(number,ch)):
            line.append(int(ch))
    return line

def read_digit(number):
    n = sys.stdin.read(1)
    while n != "":
        if(re.match(number,n)):
            return int(n)
        n = sys.stdin.read(1)


def read():
    number = re.compile("[-+]?\d+")
    # number of left players
    left_players = read_digit(number)
    # number of right players
    right_players = read_digit(number)

    # read game graphs
    left_nodes = read_digit(number)
    left = read_graph(left_nodes, number)
    right_nodes = read_digit(number)
    right = read_graph(right_nodes, number)

    # allowed moves for left

    # allowed moves for right

    # starting state for left

    # starting state for right

    # states that end the game

## Read in the graphs, allowed states, start states, and final states.
## Construct the game matrix from the graphs and initialize with the
## start states of the graph.
## Print a winning message after running the game.
def main():
    # TODO: Number of cops, number of robbers
    read()
'''
    # Game input
    left = nx.read_adjlist("left_graph.adjlist", nodetype=int, create_using=nx.DiGraph())
    right = nx.read_adjlist("left_graph.adjlist", nodetype=int, create_using=nx.DiGraph())

    # allowed moves for left and right
    # TODO: Move this to a file
    allowed_left = [(0,0),(0,1),(1,1),(1,0),(1,2),(2,1),(2,2)]
    allowed_right = [(0,0),(0,1),(1,1),(1,0),(1,2),(2,0),(2,1),(2,2)]

    # start states of left and right
    # TODO: Move this to a file
    start_left = 0
    start_right = 2

    # states that will end the game
    # TODO: Move this to a file
    final_states = [(0,0), (1,1), (2,2)]

    # Game info stored like [number of moves until win, (left_position, right_position)]
    relation_matrix = [[[sys.maxint, (i, j)] for j in range(0, len(right))] for i in range(0, len(left))]

    # Initialize the relation matrix.
    for state in final_states:
        relation_matrix[state[0]][state[1]][0] = 0

    #Run the game, record the winner.
    winner = run_game(left, right, relation_matrix)
    print "%s wins." %(winner)
    print ""
    left_strategy = gen_left_strategy(relation_matrix)
    right_strategy = gen_right_strategy(relation_matrix)
    play_game(left_strategy, right_strategy, start_left, start_right, allowed_left, allowed_right)
'''
if __name__ == "__main__":
    main()
