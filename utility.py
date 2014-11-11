from Queue import Queue
import itertools as it
import networkx as nx
import random
import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result
    return timed

@timeit
def load_graph(fname, directed = True):
	if not directed:
		g = nx.Graph()
	else:
		g = nx.DiGraph()
	with open(fname, "r") as f:
		for line in f:
			if line.startswith('#'): continue
			i, j = line.strip().split()
			g.add_edge(int(i), int(j))
	return g


@timeit
def sssp(g, v, keep_path = False):
	q = PriorityQueue()
	dist = {}

	q.put((0, v))
	if keep_path:
		dist[v] = (0, v)
	else:
		dist[v] = 0
	for i in g.nodes_iter():
		g.node[i]['visited'] = False

	if not keep_path:
		while not q.empty():
			curr = q.get()
			if g.node[curr[1]]['visited']: continue
			for node in g.neighbors(curr[1]):
				newd = curr[0] + 1
				if newd < dist.get(node, float("inf")):
					dist[node] = newd
				q.put((newd, node))
			g.node[curr[1]]['visited'] = True
	else:
		while not q.empty():
			curr = q.get()
			if g.node[curr[1]]['visited']: continue
			for node in g.neighbors(curr[1]):
				newd = curr[0] + 1
				if newd < dist.get(node, (float("inf"), None))[0]:
					if keep_path: dist[node] = (newd, curr[1])
					else: dist[node] = newd
				q.put((newd, node))
			g.node[curr[1]]['visited'] = True

	return dist

#@timeit
def bfs(g, v, keep_path = False, iterative = False):
	q = Queue()
	dist = {}

	q.put(v)
	if keep_path:
		dist[v] = (0, v)
	else:
		dist[v] = 0
	if not iterative:
		for i in g.nodes_iter():
			g.node[i]['visited'] = False

	if not keep_path:
		while not q.empty():
			curr = q.get()
			for node in g.neighbors(curr):
				if g.node[node]['visited']:
					continue
				else:
					g.node[node]['visited'] = True
					dist[node] = dist[curr] + 1
					q.put(node)
	else:
		while not q.empty():
			curr = q.get()
			for node in g.neighbors(curr):
				if g.node[node]['visited']:
					continue
				else:
					g.node[node]['visited'] = True
					dist[node] = (dist[curr][0] + 1, curr)
					q.put(node)

	return dist

def components(g):
	compo = []
	nodes = set(g.nodes())
	for i in nodes:
		g.node[i]['visited'] = False

	while len(nodes) <> 0:
		v = random.sample(nodes, 1)[0]
		d = bfs(g, v, iterative = True)
		temp = [v]
		for i in d.keys():
			temp.append(i)
			nodes.remove(i)
		compo.append(temp)
	return compo

@timeit
def get_max_degree(g):
	return max([(g.degree(i), i) for i in g.nodes_iter()])[1]

def get_unique(data, p):
	temp = None
	while temp == None:
		temp = random.choice(data)
		if random.random() > p:
			temp = None
	return temp
        
def PA(n, p):
	g = nx.Graph()
	g.add_node(0)

	visited = [0]
	current = 1
	while current < n:
		candidate = get_unique(visited, p)
		g.add_edge(current, candidate)
		visited.append(candidate)
		visited.append(current)
		current += 1
	return g

def erdos(n, p):
	g = nx.Graph()
	vertices = [i for i in range(n)]
	g.add_nodes_from(vertices)
	for i, j in it.combinations(vertices, 2):
		if random.random() < p:
			g.add_edge(i, j)
	return g
