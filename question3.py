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
    totalNodeCount = len(nodes)
    print(edgeQueue)
    e = edgeQueue.pop()  # first edge nodes form a new Partition
    print('first edge forms first partition:', e)
    e.node_from.visited = True
    e.node_to.visited = True
    partition = Partition([e.node_from, e.node_to], [e])
    nodesAdded = 2  # first edge added two nodes
    partitions = [partition]
    print(nodesAdded,totalNodeCount, len(partitions))
    while nodesAdded < totalNodeCount or len(partitions) > 1:
        newNodes = []
        toMerge = []
        while len(newNodes) == 0 and len(toMerge) == 0:
            e = edgeQueue.pop()  # get shortest edge that might add something
            print('edge to inspect:', e)
            newNodes = getUnvisitedNodes(e)
            if len(newNodes) == 0:
                toMerge = partitionsConnected(e, partitions)
        e.node_from.visited = True
        e.node_to.visited = True
        if len(newNodes) == 2:
            partition = Partition([e.node_from, e.node_to], [e])
            partitions.append(partition)
            print('+++++++added partition:', len(partitions))
        elif len(newNodes) == 1:
            newNode = newNodes[0]
            partition = findPartition(e, newNode, partitions)
            partition.addNode(newNode)
            partition.addEdge(e)
            nodesAdded += 1
            print('+++++++added node:', nodesAdded)
        else:
            toMerge[0].addPartitionWithEdge(toMerge[1], e)
            partitions.remove(toMerge[1])
            print('+++++++merged partitions:', len(partitions))
        print('+++++++', nodesAdded, len(partitions))

    return partitions[0]

def getUnvisitedNodes(edge):
    new = []
    if not edge.node_from.visited:
        # print('+++++')
        # print(edge.node_from)
        new.append(edge.node_from)
    if not edge.node_to.visited:
        # print('_-_-_-_-')
        # print(edge.node_to)
        new.append(edge.node_to)
    # print('........')
    # print(new)
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
