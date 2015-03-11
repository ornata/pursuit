import sys
import networkx as nx

'''
Reads in a digraph from stdin and returns it
input format is networkx format adjacency list
'''
def read_graph(n):
    G = nx.DiGraph()
    G.add_nodes_from([x for x in range(0, n)]) # init G with n nodes

    nodes_read = 0 

    # get the source node and then read the adjacent nodes
    while nodes_read < n:
        source = read_digit()
        target = read_line()
        edges = [(source,y) for y in target]
        G.add_edges_from(edges)
        nodes_read +=1
    return G

'''
Read until reaching \n from the current position in the stdin buffer
'''
def read_line():
    line = []
    ch = " "
    while ch != "\n" and ch != "":
        ch = sys.stdin.read(1)
        if(ch.isdigit()):
            line.append(int(ch))
    return line

'''
Read a single digit, ignoring all other characters
In the case of reaching EOF before completion, return -1
'''
def read_digit():
    num = ""
    n = sys.stdin.read(1)
    while n != "":
        if(n.isdigit()):
            while True:
                num += n
                n = sys.stdin.read(1)
                if not(n.isdigit()):
                    return int(num)
        else:
            n = sys.stdin.read(1)
    return -1

'''
Reads in a list of moves as tuples
'''
def read_move_list(n):
    nodes_read = 0
    move_list = []

    while nodes_read < n:

        # Get the vertex you start at
        source = read_digit()

        # Hit EOF, return because we're done
        if source == "":
            move_list
            return move_list

        # Get the list of vertices the source can go to
        target = read_line()

        # If there's nothing, then just return an empty list
        if target == []:
            return move_list

        # Make the list of legal moves and append it to the move list
        source_moves = [(source,y) for y in target]
        move_list.extend(source_moves)
        nodes_read += 1

    return move_list

'''
Reads in everything necessary to play the game and returns a
list.
'''
def read_game():

    # number of players
    left_players = read_digit()
    right_players = read_digit()

    # read game graphs
    left_nodes = read_digit()
    left = read_graph(left_nodes)

    right_nodes = read_digit()
    right = read_graph(right_nodes)

    # read allowed moves
    allowed_left = read_move_list(left_nodes)
    allowed_right = read_move_list(left_nodes)

    # read final states
    n_final_states = read_digit()
    final_states = read_move_list(n_final_states)

    # read starting positions
    start_left = read_digit()
    start_right = read_digit()

    return [left,right,allowed_left,allowed_right,final_states,start_left,start_right]