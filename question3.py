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

"""This algorithm computes a minimum spanning tree for the input graph
by adding edges to the tree shortest edge first.  That is, the list of
all edges in the graph is sorted and the shortest edge is removed:
  - If this edge connects two nodes that are not yet part of the tree
    then the edge and its nodes are remembered as a partition to be
    connected to the rest of the tree later.
  - If this edge connects a node in a known partition to a node not yet in the
    tree, then this edge and the new node are added to this partition.
  - If this edge connects nodes in two different known partitions
    the partitions are merged and the edge added.
  - If this edge connects two nodes already visited, the edge is discarded.

This process is repeated for each edge until all nodes from the graph are 
in the tree and all partitions have been merged.  This assumes that the input
graph is connected and that it does not matter which direction edges are 
traversed.

Each partition maintains a dictionary of its nodes so it is efficient to 
test whether a given node is contained in the partition.

Because this algorithm adds each node exactly
once with an edge connecting it to the rest, a tree is formed.  Because
the tree is constructed shortest edge first, we know it is a minimum
spanning tree.  I think this could be proved by induction but I'll skip
the proof here."""

"""Complexity of this algorithm depends on the number of nodes n and the
number of edges e.  In the initial sort of the edges uses the default 
Python sort function for lists, which is O(e(log e)).  The main loop adds
one or two nodes to the tree each loop so in the worst case it executes
n times.  Inside the main loop, the search for the next edge that grows
the tree consists of:
  - popping from the edgeQueue which is O(1)
  - getUnvisitedNodes which is O(1)
  - sometimes calling partitionsConnected, which iterates through the list
    of known partitions, checking their dictionaries for the associated nodes.
    The python dictionary lookup is O(1) and the number of partitions begins
    at 1 and can never be bigger than the number of n/2 since each
    partition has at least 2 nodes in it.  In the worst case this is O(n).
And also in the main loop, the growing of the tree consists of:
  - adding a partition which is O(1), or
  - finding a partition to add a node and edge, which is O(n), or
  - merging two partitions, which O(n + e) in the worst case

Putting this together, I get:
  e(log e) + n( 1 or n or n+e )

When n is large, this is O(n^2), but if e is much larger than n then the n*e
term would be more significant.
"""

class Node(object):
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.visited = False

    def __str__(self):
        return str(self.value)
        # + ' edges: ' + str(self.edges) + ' visited: ' + str(self.visited)

    def __repr__(self):
        return 'Node('+self.__str__()+')'

class Edge(object):
    def __init__(self, value, node_from, node_to):
        self.value = value
        self.node_from = node_from
        self.node_to = node_to

    def __str__(self):
        return 'value: ' + str(self.value) + ' from: ' + str(self.node_from) + ' to: ' + str(self.node_to)

    def __repr__(self):
        return 'Edge('+self.__str__()+')'

class Graph(object):
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges

    def edgesSum(self):
        sum = 0
        for e in self.edges:
            sum += e.value
        return sum

class Partition(Graph):
    """constructing a partition, must take care to copy input nodes and
    edges, so this algorithm does not modify the original graph while
    constructing a tree.

    Also, create nodeMap dictionary to lookup nodes by name, so test
    for inclusion is easy and efficient."""
    def __init__(self, i_nodes, i_edges):
        self.nodes = []
        self.edges = []
        self.nodeMap = {}
        for n in i_nodes:
            self.addNode(self.copyNode(n))
        for e in i_edges:
            self.addEdge(self.copyEdge(e))

    def copyNode(self, node):
        return Node(node.value)

    def addNode(self, node):
        self.nodes.append(node)
        self.remember(node)

    def remember(self, node):
        """support lookup by value"""
        self.nodeMap[node.value] = node

    def addPartitionWithEdge(self, partition, edge):
        for n in partition.nodes:
            self.nodes.append(n)
        for e in partition.edges:
            self.edges.append(e)
        self.addEdge(self.copyEdge(edge))

    def copyEdge(self, edge):
        f = self.lookup(edge.node_from)
        t = self.lookup(edge.node_to)
        return Edge(edge.value, f, t)

    def addEdge(self, edge):
        f = self.lookup(edge.node_from)
        t = self.lookup(edge.node_to)
        f.edges.append(edge)
        t.edges.append(edge)
        self.edges.append(edge)

    def lookup(self, node):
        return self.nodeMap[node.value]

    def contains(self, node):
        return node.value in self.nodeMap

    def __str__(self):
        s = ''
        for n in self.nodes:
            s += str(n) + ', '
        return s

    def __repr__(self):
        return 'Partition('+self.__str__()+')'


def question3(G):
    # nmap is a dictionary for node lookup by id
    nmap = {}
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

    """Now compute minimum spanning tree"""
    edgeQueue = sorted(edges, key=lambda edge: edge.value, reverse=True)
    totalNodeCount = len(nodes)
    e = edgeQueue.pop()  # first edge nodes form a new Partition
    e.node_from.visited = True
    e.node_to.visited = True
    partition = Partition([e.node_from, e.node_to], [e])
    nodesAdded = 2  # first edge added two nodes
    partitions = [partition]
    while nodesAdded < totalNodeCount or len(partitions) > 1:
        newNodes = []
        toMerge = []
        while len(newNodes) == 0 and len(toMerge) == 0:
            e = edgeQueue.pop()  # get shortest edge that might add something
            newNodes = getUnvisitedNodes(e)
            if len(newNodes) == 0:
                toMerge = partitionsConnected(e, partitions)
        e.node_from.visited = True
        e.node_to.visited = True
        if len(newNodes) == 2:
            partition = Partition([e.node_from, e.node_to], [e])
            partitions.append(partition)
        elif len(newNodes) == 1:
            newNode = newNodes[0]
            partition = findPartition(e, newNode, partitions)
            partition.addNode(newNode)
            partition.addEdge(e)
            nodesAdded += 1
        else:
            toMerge[0].addPartitionWithEdge(toMerge[1], e)
            partitions.remove(toMerge[1])

    return partitions[0]

def getUnvisitedNodes(edge):
    new = []
    if not edge.node_from.visited:
        new.append(edge.node_from)
    if not edge.node_to.visited:
        new.append(edge.node_to)
    return new

def partitionsConnected(edge, partitions):
    touchedByEdge = []
    for p in partitions:
        if p.contains(edge.node_from) or p.contains(edge.node_to):
            touchedByEdge.append(p)
        if len(touchedByEdge) == 2:
            return touchedByEdge
    return []

def findPartition(edge, newNode, partitions):
    if edge.node_from == newNode:
        oldNode = edge.node_to
    else:
        oldNode = edge.node_from
    for p in partitions:
        if p.contains(oldNode):
            return p
    return None

def test(g, expect):
    print(g)
    print('expect {}, actual {}'.format(expect, question3(g).edgesSum()))

g = {'A': [('B', 2)],
 'B': [('A', 2), ('C', 5)],
 'C': [('B', 5)]}
test(g, 7)

g = {
    'A': [('B', 3), ('F', 5), ('C', 2)],
    'B': [('A', 3), ('C', 4), ('D', 1)],
    'C': [('A', 2), ('B', 4), ('E', 1)],
    'D': [('B', 1), ('E', 5), ('F', 1)],
    'E': [('C', 1), ('D', 5), ('F', 1)],
    'F': [('E', 1), ('A', 5), ('D', 1)],
}
test(g, 6)
