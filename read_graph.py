import sys
import networkx as nx

'''
Reads in a digraph from stdin and returns it
input format is networkx format adjacency list
'''
def read_graph(n):
    G = nx.DiGraph()
    G.add_nodes_from([x for x in range(0, n)]) # init G with n nodes

    for i in range(0, n):
        row = sys.stdin.readline() # read in the row as a list
        verts = row.split() # split on whitespace
        verts = map(int,verts) 
        edges = [(int(verts[0]),int(y)) for y in verts[1:]]
        G.add_edges_from(edges)
    return G

'''
Read a single digit, ignoring all other characters
In the case of reaching EOF before completion, return -1
'''
def read_digit():
    num = ""
    n = sys.stdin.read(1)
    while n != "": # read until EOF
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
    i = 0
    while True:
        if i == n:
            break
        row = sys.stdin.readline().splitlines()
        if row == ['']:
            continue
        verts = row[0].split()
        verts = map(int,verts)
        moves = [(verts[0],y) for y in verts[1:]]
        move_list.extend(moves)
        i += 1

    return move_list

'''
Reads in everything necessary to play the game and returns a
list.
'''
def read_game():

    # read game graphs
    left_nodes = read_digit()
    if left_nodes == -1:
        return None

    left = read_graph(left_nodes)
    if left == None:
        return None

    right_nodes = read_digit()
    if right_nodes == -1:
        return None

    right = read_graph(right_nodes)
    if right == None:
        return None

    # read allowed moves
    allowed_left = read_move_list(left_nodes)
    if allowed_left == []:
        return None

    allowed_right = read_move_list(left_nodes)
    if allowed_right == []:
        return None

    # read final states
    n_final_states = read_digit()
    if n_final_states == -1:
        return None

    final_states = read_move_list(n_final_states)
    if final_states == []:
        return None

    # read starting positions
    start_left = read_digit()
    if start_left == -1:
        return None

    start_right = read_digit()
    if start_right == -1:
        return None

    # successfully read a game, return the entire list
    return [left,right,allowed_left,allowed_right,final_states,start_left,start_right]