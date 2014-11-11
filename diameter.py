import networkx as nx
import sys
import random
from utility import *

def check_connectivity(bfs_tree):
	disconnected = []
	for node, dist in bfs_tree.items():
		if dist == float("inf"):
			disconnected.append(node)
			del bfs_tree[node]
	return disconnected

def calculate_diameter(g, directed):
	# Crescenzi, Pierluigi, et al. "Finding the Diameter in Real-World Graphs."
	# Algorithms-ESA 2010. Springer Berlin Heidelberg, 2010. 302-313.

	nodes = g.nodes()
	max_compo = 0
	dia = 0
	D = 0

	while len(nodes) <> 0:
		# Doublesweep lower-bound
		r = random.sample(nodes, 1)[0]
		bfs_r = bfs(g, r)

		for i in bfs_r: nodes.remove(i)
		temp = len(bfs_r)
		'''
		if len(bfs_r) <> g.number_of_nodes():
			print "Disconnected", len(bfs_r)
		'''

		# vertex with maximum distance
		a, ecc_a = max(bfs_r.iteritems(), key = lambda x: x[1])
		#print "Got a: ", a, " ", ecc_a
		del bfs_r

		bfs_a = bfs(g, a, keep_path = True)
		b = max(bfs_a.iteritems(), key = lambda x: x[1][0])
		ecc_b = b[1][0]
		b = b[0]
		#print "Found b: ", b, ecc_b

		# Finding midway node
		dist = 0
		curr = b
		while dist < (ecc_b / 2):
			prev = bfs_a[curr][1]	# we can't write curr = bfs_a[curr][1]
			curr = prev
			dist += 1
		u = curr
		#print "Midway: ", u, " ", dist
		del bfs_a

		bfs_u = bfs(g, u)
		ecc_u = max(bfs_u.iteritems(), key = lambda x: x[1])[1]
		#print "Found u: ", u, " ", ecc_u
		F_u = [i for i, j in bfs_u.items() if j == ecc_u]
		#print "F_u: ", len(F_u)

		if len(F_u) <> 1:
			B_u = 0
			for i in F_u:
				bfs_i = bfs(g, i)
				ecc = max(bfs_i.iteritems(), key = lambda x: x[1])[1]
				if B_u < ecc:
					B_u = ecc
			#print B_u
			if B_u >= (2 * ecc_u - 1):
				dia = B_u
			elif B_u < (2 * ecc_u - 1):
				dia = 2 * ecc_u - 2
		else:
			dia = ecc_u

		if temp > max_compo:
			max_compo = temp
			D = dia
	return D

if __name__ == "__main__":
	#g = PA(1000, 0.01)
	#g = nx.barabasi_albert_graph(1000, 4)
	#directed = False
	g = load_graph(sys.argv[1], True if sys.argv[2] == 'd' else False)
	print calculate_diameter(g, False)

	'''
	P = [0.0004, 0.0008, 0.001, 0.008, 0.01]
	for p in P:
		g = erdos(1000, p)
		print "%f\t%d" % (p, calculate_diameter(g, False))
	'''
