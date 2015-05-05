import sys
import networkx as nx
import read_graph as rg
import collections
import copy

SHOW_MAT = False #show matrix updates

'''
print_rel_mat
-----------------------------------------------------------------------------
Formatted printing for relation matrix
'''
def print_rel_mat(mat):
    for key, value in mat.iteritems():
        print ""
        for elem in value:
            if elem == sys.maxint:
                print "-",
            else:
                print elem,
    print ""

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

Choose the smallest possible label out of each "better" play left could make.
If it is not possible for left to shorten the game no matter what right does, we
can't say anything about a guaranteed better strategy and so we can't update anything.
Returns True if the position (left, right) was relabeled, False otherwise.
'''
def relabel(rel_mat, l, r, allowed_left, allowed_right, label):

    # The current positions have already been labelled, so nothing can be updated.
    if label != sys.maxint:
        return False

    moves_countered = 0
    candidate_labels = collections.deque() # Candidates for relabeling
    append_candidate_label = candidate_labels.append # Avoid repeated evaluation of append
    min_label = label

    # Which moves can each of the left players make?
    legal_left = set()
    legal_right = allowed_right[r][1:]

    # Right can't legally make a move anymore -- if we can move here, we can win
    if len(legal_right) == 0:
        return False


    for legal in allowed_left:
        for i in range(0, len(l)):
            if l[i] == legal[0]: # i-th left player can move to some spot
                # Add each of the possible moves:
                for move in legal[1:]:
                    new_pos = list(l)
                    new_pos[i] = move
                    legal_left.add(tuple(new_pos))

    if len(legal_left) == 0:
        return False

    # Try to counter every move the right player could make
    for right_move in legal_right:
        for left_move in legal_left:
            if rel_mat[left_move][right_move] < label:
                    append_candidate_label(rel_mat[left_move][right_move]+1)
                    moves_countered += 1
                    break

    if moves_countered < len(allowed_right[r])-1:
        return False

    rel_mat[l][r] = min(candidate_labels)
    return True



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

    lnodes = left.nodes()
    rnodes = right.nodes()
    for i in xrange(0, len(left)):
        for j in xrange(0, len(right)):
            #print rel_mat[lnodes[i]][rnodes[j]]
            updated_entry = relabel(rel_mat, lnodes[i], rnodes[j], allowed_left, allowed_right, rel_mat[lnodes[i]][rnodes[j]]) 
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

    for key, value in rel_mat.iteritems():
        for entry in value:
            if sys.maxint == entry:
                return "Right"

    # There are no unlabelled rows.
    return "Left"


'''
update_nodes
-----------------------------------------------------------------------------
Helper function for flattening out the tuples that result from taking the
categorical product.
'''
def update_nodes(node, new_node, append_to_new_node):
    if type(node) is not tuple:
        append_to_new_node(node)
        return new_node

    for entry in node:
        if type(entry) is tuple:
            update_nodes(entry, new_node)
        else:
            append_to_new_node(entry)

    return new_node
         
'''
get_nbrs
-----------------------------------------------------------------------------
Helper function for finding Right's winning strategy.
'''       
def get_nbrs(row, parent_list, relation_matrix, allowed, updated, count, append_to_updated):
    if len(parent_list) == 0:
        return
    nbrs = collections.deque()
    append_to_nbrs = nbrs.append

    for i in range(0, len(allowed)):
        for j in range(0, len(allowed[i])):
            if allowed[i][j] in parent_list and i not in updated:
                append_to_nbrs(i)
                append_to_updated(i)
                row[i] = count

    if len(set(nbrs)) == 0:
        return

    get_nbrs(row, set(nbrs), relation_matrix, allowed, updated, count+1, append_to_updated)

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

        k = 1 # number of left players
        lgraph = left

        # Take the k-fold categorical product of the graph
        for i in range(1,k):
            lgraph = nx.tensor_product(lgraph,left)
        left = lgraph

        # Workaround for networkx's built-in categorical product
        new_labels = {}
        for n in left.nodes():
            new = collections.deque()
            append_to_new = new.append
            update_nodes(n, new, append_to_new)
            new_labels[n] = tuple(new)

        nx.relabel_nodes(left, new_labels, copy=False)

        # Put allowed_right in a format that makes sense. a list of (current pos, next pos)
        rmoves = collections.deque()
        append_to_rmoves = rmoves.append
        for move in allowed_right:
            x = move[0]
            for m2 in move[1:]:
                y = m2
                append_to_rmoves([(x,y), sys.maxint])

        # Construct a dictionary with left's position(s) as keys, right's as values
        relation_matrix = {}
        for v in left.nodes():
            relation_matrix[v] = [sys.maxint] * len(right)

        # Initialize the dict with 0's at every final state
        # when do we have a final stat
        for key, value in relation_matrix.iteritems():
            for f in final_states:
                if f[0] in key: # there is a left player matching the position
                    for i in range(0, len(value)):
                        if i == f[1]:
                            value[i] = 0

        #Run the game, record the winner.
        winner = fill_matrix(left, right, relation_matrix, allowed_left, allowed_right)
        print "\nWinner: %s \n" %(winner)

        strategy = collections.OrderedDict(sorted(relation_matrix.items(), key = lambda t: t[0]))

        # Left's strategy: How many moves would it take for left to get to a node labelled 0?
        if winner == 'Left':
            for key, value in strategy.iteritems():
                print key,
                for entry in value:
                    print entry,
                print ""

        # Right's strategy: How many moves would it take for right to get to a node labelled sys.maxint?
        if winner == 'Right':
            updated = collections.deque()
            append_to_updated = updated.append
            for key, value in strategy.iteritems():
                row = [0]*right.number_of_nodes() # best case: 0 moves
                for i in range(0, len(value)):
                    if value[i] == 0: # right would lose at this point
                        append_to_updated(i)
                        row[i] = -1

                    if value[i] == sys.maxint: # right would win here
                        append_to_updated(i)
                        row[i] = 0
                        neighbours = collections.deque()
                        append_to_neighbours = neighbours.append

                        # recursively relabel each of the nodes which have a move leaving into i
                        for j in range(0, len(allowed_right)):
                            for k in range(0, len(allowed_right[j])):
                                if allowed_right[j][k] == i:
                                    append_to_neighbours(j)
                        get_nbrs(row, set(neighbours), relation_matrix, allowed_right, updated, 1, append_to_updated)

                # print out the labels
                print key,
                for entry in row:
                    print entry,
                print ""

        game = []

if __name__ == "__main__":
    main()