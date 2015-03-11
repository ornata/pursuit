import networkx as nx

def print_g(l):
	for x in range(0, n):
		print x,
		print " ",
		for y in range(0,len(l[x])):
			print y,
			print " ",
		print ""

n = 20
G = nx.fast_gnp_random_graph(n, 0.7, None, True)
l = G.adjacency_list()

print 1
print 1
print ""
print n
print_g(l)
print ""
print n
print_g(l)

print ""
print_g(l)
print ""
print_g(l)

print n
print ""
for i in range(0,n):
	print i,
	print " ",
	print i

print ""
print 0
print 2

