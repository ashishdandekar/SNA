import networkx as nx
import sys
import random
from utility import *
import matplotlib.pyplot as plt

def max_degree_victim(g):
	return get_max_degree(g)

def random_victim(g):
	return random.choice(g.nodes())

def start_epidemic(g, v):
	# SIR epidemic model is used
	profile = {}
	N = float(g.number_of_nodes())
	INFECTED = {}	# {victim_id : recovery time}

	INFECTED[v] = 0
	victims = len(INFECTED)
	t = 1
	while 1:
		for i, j in INFECTED.items():
			SUSCEPTIBLE = g.neighbors(i)
			if len(SUSCEPTIBLE) == 0 or INFECTED[i] == len(SUSCEPTIBLE):
				# Can not infect anyone
				continue

			#v = random.choice(SUSCEPTIBLE)
			#if v not in INFECTED:
			#	INFECTED[i] += 1
			#	INFECTED[v] = 0
			for _ in range(len(SUSCEPTIBLE)):
				v = random.choice(SUSCEPTIBLE)
				if v not in INFECTED:
					INFECTED[i] += 1
					INFECTED[v] = 0
					break

		if victims == g.number_of_nodes():
			#print "Can not be spread any further"
			break
		else:
			victims = len(INFECTED)
			profile[t] = victims / float(g.number_of_nodes())
			print "%d\t\t%f" % (t, profile[t])
			t += 1

	return profile 

if __name__ == "__main__":
	g = load_graph(sys.argv[1], True if sys.argv[2] == 'd' else False)
	#g = PA(1000, 0.01)
	#g = erdos(1000, 0.01)
	#g = nx.barabasi_albert_graph(1000, 4)
	
	#degree = {i : g.degree(i) for i in g.nodes_iter()}
	#rank = {}
	#for i, j in g.edges_iter():
	#	rank[i] = rank.get(i, 0) + degree[j]
	#	rank[j] = rank.get(j, 0) + degree[i]

	#max_v, max_deg = max(degree.items(), key = lambda x: x[1])
	#print 'MAX_DEGREE', max_deg
	#max_degree_set = [i for i in g.nodes_iter() if degree[i] == max_deg]

	#v = random.sample(max_degree_set, 1)[0]
	#p, r = start_epidemic(g, v)
	#plt.plot(*zip(*p.items()), color = 'b')

	#plt.figure("random")
	v = random_victim(g)
	p, r = start_epidemic(g, v)
	#plt.plot(*zip(*p.items()), color = 'r')

	#plt.figure("max_degree")
	#tot_time = 0
	#tot_frac = 0
	#for i in range(7):
	#	v = random.sample(max_degree_set, 1)[0]
	#	#v_dash = random.sample(g.neighbors(v), 1)[0]
	#	p = start_epidemic(g, v)
	#	plt.plot(*zip(*p.items()))
	#	plt.xlabel("time")
	#	plt.ylabel("fraction of infected population")
	#	max_time = max(p.keys())
	#	#print "ITERATION %d: %d \t %d" % (i, max_time, p[max_time])
	#	tot_time += max_time
	#	tot_frac += p[max_time]
	#print "Average time(max degree): ", tot_time / float(7)
	#print "Fraction covered(max degree): ", tot_frac / float(7)

	#plt.figure("random")
	#tot_time = 0
	#tot_frac = 0
	#for i in range(7):
	#	v = random_victim(g)
	#	p = start_epidemic(g, v)
	#	plt.plot(*zip(*p.items()))
	#	plt.xlabel("time")
	#	plt.ylabel("fraction of infected population")
	#	plt.suptitle('Already "informed" neighbours excluded')
	#	max_time = max(p.keys())
	#	tot_time += max_time
	#	tot_frac += p[max_time]
	#print "Average time(random): ", tot_time / float(7)
	#print "Fraction covered(max degree): ", tot_frac / float(7)

	#plt.figure("popularity")
	#tot_time = 0
	#tot_frac = 0
	#for i in range(7):
	#	v = min(rank.items(), key = lambda x: x[1])[0]
	#	p = start_epidemic(g, v)
	#	plt.plot(*zip(*p.items()))
	#	plt.xlabel("time")
	#	plt.ylabel("fraction of infected population")
	#	max_time = max(p.keys())
	#	#print "ITERATION %d: %d \t %d" % (i, max_time, p[max_time])
	#	tot_time += max_time
	#	tot_frac += p[max_time]
	#print "Average time(max popular): ", tot_time / float(7)
	#print "Fraction covered(max degree): ", tot_frac / float(7)
	#plt.show()
