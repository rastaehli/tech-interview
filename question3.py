"""Question 3
Given an undirected graph G, find the minimum spanning tree within G. A minimum 
spanning tree connects all vertices in a graph with the smallest possible total 
weight of edges. Your function should take in and return an adjacency list 
structured like this:

{'A': [('B', 2)],
 'B': [('A', 2), ('C', 5)], 
 'C': [('B', 5)]}

Vertices are represented as unique strings. The function definition should be 
question3(G)
"""

class Node(object):
    def __init__(self, value):
        self.value = value
        self.edges = []

class Edge(object):
    def __init__(self, value, node_from, node_to):
        self.value = value
        self.node_from = node_from
        self.node_to = node_to

class Graph(object):
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges


def question3(G):
	# nmap is a dictionary for node lookup by id
    self.nmap = {}
    nodes = []
    edges = []

	for id1 in G:
		if not id1 in nmap:
			nmap[id1] = Node(id1)
			nodes.append(nmap[id1])
		for id2, weight in G[id1]:
			if not id2 in nmap:
				nmap[id2] = Node(id2)
				nodes.append(nmap[id2])
			edge = Edge(weight, nmap[id1], nmap[id2])
			edges.append(edge)
			nmap[id1].edges.append(edge)
			nmap[id2].edges.append(edge)

	graph = Graph(nodes, edges)
	#handle trivial case of graph with one or fewer nodes
	if len(nodes) < 2:
		return graph

	"""Now compute minimum spanning tree by adding edges to unvisited
	nodes shortest edge first until all nodes have been visited and all 
	partitions are connected.  That is, when each edge is added, it either 
	connects a new node to an existing group of connected, visited, nodes 
	(a partition) or it forms a new partition of the two nodes it connects.  
	We keep a list of partitions, each with a dictionary
	of its nodes so it is efficient to test whether a given 
	node is in the partition.  

	Because this algorithm adds each node exactly
	once with an edge connecting it to the rest, a tree is formed.  Because
	the tree is constructed shortest edge first, we know it is a minimum
	spanning tree.  I think this could be proved by induction but I'll skip
	the proof here."""
	edgeQueue = sorted(edges, key=lambda edge: edge.value, reverse=True)
	nodesAdded = 0
	totalNodeCount = len(nodes)
	e = edgeQueue.pop()
	partition = Partition([e.node_from.vcopy, e.node_to.vcopy], [e])
	partitions = [partition]
	while nodesAdded < totalNodeCount and len(partitions) > 1:
		newNodes = []
		newPartitionsConnected = []
		while len(newNodes) == 0 and len(newPartitionsConnected) == 0:
			e = edgeQueue.pop()  # get shortest edge that might add something
			newNodes = getUnvisitedNodes(e)
			if len(newNodes) == 0:
				newPartitionsConnected = partitionsConnected(e, partitions)
		if len(newNodes) == 2:
			partition = Graph([e.node_from, e.node_to], [e])
			partitions.append(partition)
		elif len(newNodes) == 1:
			partition = findPartition(newNodes[0], partitions)
			partition.addNodeWithEdge(newNodes[0], e)
		else
			partitionsConnected[0].addPartitionWithEdge(partitionsConnected[1], e)

	return partitions[0]

class Partition(Graph):
	"""constructing a partition, must take care to copy input nodes and
	edges, so this algorithm does not modify the original graph while
	constructing a tree.

	Also, be sure to add a dictionary to lookup nodes by name, so test
	for inclusion is easy and efficient."""
