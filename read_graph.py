import re
import sys
import networkx as nx

## Reads in a digraph from stdin and returns it
def read_graph(n, number):
    G = nx.DiGraph()
    G.add_nodes_from([x for x in range(0, n)]) # init G with n nodes

    nodes_read = 0 

    while nodes_read < n:
        source = read_digit(number)
        target = read_line(number)
        edges = [(source,y) for y in target]
        G.add_edges_from(edges)
        nodes_read +=1

    return G

## Read until reaching \n from the current position in the stdin buffer
def read_line(number):
    line = []
    ch = " "
    while ch != "\n" and ch != "":
        ch = sys.stdin.read(1)
        if(re.match(number,ch)):
            line.append(int(ch))
    return line

## Read a single digit, ignoring all other characters
def read_digit(number):
    n = sys.stdin.read(1)
    while n != "":
        if(re.match(number,n)):
            return int(n)
        n = sys.stdin.read(1)
    return -1

## Reads in a list of moves as tuples
def read_move_list(n, number):
    nodes_read = 0
    move_list = []

    while nodes_read < n:

        source = read_digit(number)

        if source == "":
            move_list
            print "Ended at source"
            print move_list
            return move_list

        target = read_line(number)

        if target == []:
            print "Ended at target"
            print move_list
            return move_list

        source_moves = [(source,y) for y in target]
        for move in source_moves:
            move_list.append(move)
        nodes_read += 1
    print "Ended normally"
    print move_list
    return move_list

## Reads in everything necessary to play the game and returns
## it all in a list
def read_game():
    # used in other read functions
    number = re.compile("[-+]?\d+")
    
    # number of players
    left_players = read_digit(number)
    right_players = read_digit(number)

    # read game graphs
    left_nodes = read_digit(number)
    left = read_graph(left_nodes, number)

    right_nodes = read_digit(number)
    right = read_graph(right_nodes, number)

    # read allowed moves
    allowed_left = read_move_list(left_nodes, number)
    allowed_right = read_move_list(left_nodes, number)

    # read final states
    n_final_states = read_digit(number)
    final_states = read_move_list(n_final_states, number)

    # read starting positions
    start_left = read_digit(number)
    start_right = read_digit(number)

    return [left,right,allowed_left,allowed_right,final_states,start_left,start_right]