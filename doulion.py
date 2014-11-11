import sys
import heapq
import random
import networkx as nx
from Queue import PriorityQueue
import itertools as it
import time                                                
from utility import *


@timeit
def sparsify(g, p):
	L = []
	for e in g.edges_iter():
		if random.random() < p:
			L.append(e)
	g.remove_edges_from(L)
	del L

@timeit
def count_triangles(g, directed):
	if directed:
		pass
	else:
		count = 0
		for v in g.nodes_iter():
			for pair in it.combinations(g.neighbors(v), 2):
				if g.has_edge(*pair): count += 1
	return count

def triangles(g, directed):
	# Tsourakakis, Charalampos E., et al. "Doulion: counting triangles in massive graphs with a coin."
	# Proceedings of the 15th ACM SIGKDD international conference on Knowledge discovery and data mining.
	# ACM, 2009.

	# It is better to take a copy of the graph prior to this
	p = 0.45
	sparsify(g, p)

	if directed:
		return count_triangles(g, directed) * ((1 / p) ** 3) * (1 / 3.0)
	else:
		return count_triangles(g, directed) * ((1 / p) ** 3) * (1 / 6.0)

if __name__ == "__main__":
	'''
	Code to load the graph

	if len(sys.argv) <> 3:
		print "Usage: python %s <fname> <directed/undirected>" % sys.argv[0]
		sys.exit(1)

	if sys.argv[2] == 'u':
		directed = False
	elif sys.argv[2] == 'd':
		directed = True
	else:
		print "Wrong Argument"
	# youtube answer is : 1536932.0
	g = load_graph(sys.argv[1], directed)
	'''
	g = PA(1000, 0.03)
	#g = nx.barabasi_albert_graph(1000, 4)
	#g = erdos(1000, 0.01)

	#P = [0.0004, 0.0008, 0.001, 0.008, 0.01]
	#for p in P:
	#	g = PA(1000, p)
	#	print "%f\t%d" % (p, triangles(g, False))
	print triangles(g, False)
