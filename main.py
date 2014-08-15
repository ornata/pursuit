import sys
import itertools
import time
import networkx as nx

# Formatted printing for relation matrix
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

## Read in the graphs, allowed states, start states, and final states.
## Construct the game matrix from the graphs and initialize with the
## start states of the graph.
## Print a winning message after running the game.
def main():
    # Game input
    left = nx.read_adjlist("left_graph.adjlist", nodetype=int, create_using=nx.DiGraph())
    right = nx.read_adjlist("left_graph.adjlist", nodetype=int, create_using=nx.DiGraph())
    
    round_summary = nx.tensor_product(left,right)

    # allowed moves for left and right
    # TODO: Move this to a file
    allowed_left = [(0,0),(0,1),(1,1),(1,0),(1,2),(2,1),(2,2)]
    allowed_right = [(0,0),(0,1),(1,1),(1,0),(1,2),(2,1),(2,2)]

    # start states of left and right
    # TODO: Move this to a file
    start_left = 0
    start_right = 2

    # states that will end the game
    # TODO: Move this to a file
    final_states = [(0,0), (1,1), (2,2)]

    relation_matrix = [[[sys.maxint, (i, j)] for j in range(0, len(right))] for i in range(0, len(left))]

    # Initialize the relation matrix.
    for state in final_states:
        relation_matrix[state[0]][state[1]][0] = 0

    #Run the game, record the winner.
    winner = run_game(left, right, relation_matrix)
    print "%s wins." %(winner)
    print ""

if __name__ == "__main__":
    main()
