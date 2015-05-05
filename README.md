#pursuit

Decide who wins a finite, discrete pursuit game like cops ("left players") and robbers ("right players") on a graph. This code is an implementation of a result by Anthony Bonato and Gary MacGillivray in "A General Framework for Discrete-Time Pursuit Games". The specific result is that there exists an O(n^{2k + 2}) algorithm deciding the winner of a (discrete-time) pursuit game on a graph with k left players (or right players).

####Input format:
Graphs (and move lists) are input using the standard NetworkX adjacency list format. That is, for every vertex in the graph, you write

> source target target target... target

on a new line.

To input a game, you need
1. Left's game graph
2. Right's game graph
3. The moves Left can legally make over the course of the game
4. The moves Right can legally make over the course of the game
5. The states that cause Left to catch Right
6. The state that Left starts at and the state that Right starts at

Entry 6 isn't really necessary, but if you wanted to visualize the game, you would need a starting state.

##### Left and Right's Graphs
Left and Right's graphs are represented using adjacency lists, and the number of nodes for the graph.

1. number of nodes in the graph
2. adjacency list for the graph

##### Allowed moves
The format for 3 and 4 is just an adjacency list. The "source" node in this case represents the state that Right or Left is currently in. The "target" nodes are the nodes that Left or Right can move to.

##### Final States

On a new line, for every possible final state,

> left right

##### Starting States
Starting states are represented as single integers on a line representing the node at which Left (or Right) starts at.

#### Caveats
* Left's and Right's graphs must be the same size. They are playing on the same graph after all!
