import networkx as nx

def print_g(G):
	for line in nx.generate_adjlist(G):
		print line
	print ""

ngames = 1
for i in range(0,ngames):
	n = 10
	#G = nx.fast_gnp_random_graph(n, 0.7, None, True)
	G = nx.binomial_graph(n, 0.3, None, True)
	print n # number of verts
	print_g(G) # left's game graph
	print n # number of verts
	print_g(G) # right's game graph
	print_g(G) # allowed moves for left
	print_g(G) # allowed moves for right
	print n # number of final states
	for i in range(0,n): # final states
		print i,
		print "",
		print i
	print ""
	print 0 # starting positions
	print 2
	print ""

