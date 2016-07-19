"""solutions.py contains the required functions named "question1",
"question2", et cetera.  Additional classes and helper functions are
included first.  The test cases are included at the bottom.
"""

# ======= supporting classes ======================================

class Palindrome(object):
    """Also serves as item in doubly linked list"""
    def __init__(self, s, l):
        self.start = s
        self.length = l
        self.next = None
        self.prev = None


class LinkedList(object):
    def __init__(self):
        self.head = None

    def insert(self, item):
        """insert at front"""
        if self.head:
            self.head.prev = item
        item.next = self.head
        self.head = item

    def remove(self, item):
        if self.head == item:
            self.head = item.next
        else:
            item.prev = item.next


class Node(object):
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.visited = False

    def __str__(self):
        return 'Node:'+str(self.value)
        # + ' edges: ' + str(self.edges) + ' visited: ' + str(self.visited)

    def __repr__(self):
        return 'Node('+self.__str__()+'['+str(self.edges)+'])'

    def equals(self, node):
        return self.value == node.value

    def addEdge(self, edge):
        otherNode = other(self, edge)  # get other node from edge
        for e in self.edges:
            if edge.value == e.value and otherNode == e.node_to:
                return  e  # edge already added
        newEdge = Edge(edge.value, self, otherNode)
        self.edges.append(newEdge)

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
            self.addNode(n)
        for e in i_edges:
            self.addEdge(e)

    def copyNode(self, node):
        return Node(node.value)

    def addNode(self, node):
        copy = self.copyNode(node)
        self.nodes.append(copy)
        self.remember(copy)

    def remember(self, node):
        """support lookup by value"""
        self.nodeMap[node.value] = node

    def addPartitionWithEdge(self, partition, edge):
        for n in partition.nodes:
            self.nodes.append(n)
        for e in partition.edges:
            self.edges.append(e)
        self.addEdge(edge)

    def copyEdge(self, edge):
        f = self.lookup(edge.node_from)
        t = self.lookup(edge.node_to)
        return Edge(edge.value, f, t)

    def addEdge(self, edge):
        copy = self.copyEdge(edge)
        copy.node_from.addEdge(copy)
        copy.node_to.addEdge(copy)
        self.edges.append(copy)

    def lookup(self, node):
        return self.nodeMap[node.value]

    def contains(self, node):
        return node.value in self.nodeMap

    def __str__(self):
        s = ''
        for n in self.nodes:
            s += str(n) + ', '
        for e in self.edges:
            s += str(e.value) + ', '
        return s

    def __repr__(self):
        return 'Partition('+self.__str__()+')'


# ======= global helper functions =================================

def anagramFound(s, t, p):
    """return true if an anagram of t is found at position p of s"""
    letters = lettersOf(t)  # take letters from t in any order to match s at p
    while len(letters) > 0:
        # print(s[p], letters)
        if s[p] in letters:
            # print('letter found')
            letters.remove(s[p])
            p += 1
        else:
            return False
    return True

def lettersOf(t):
    # print('getting lettersOf {}'.format(t))
    list = []
    for l in t:
        # print('adding letter {}'.format(l))
        list.append(l)
    return list

def canGrow(p, length):
    # True if index before and after are valid
    return (p.start > 0) and (p.start + p.length < length)

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

def other(node, edge):
    if edge.node_from.equals(node):
        return edge.node_to
    return edge.node_from

def adjacencyList(tree):
    aListMap = {}
    for n in tree.nodes:
        l = []
        for e in n.edges:
            l.append((other(n,e).value, e.value))
        aListMap[n.value] = l
    return aListMap

def sumEdges(adjacencyListMap):
    edgeValues = {}
    for n in adjacencyListMap:
        for tuple in adjacencyListMap[n]:
            # non-directional edge id: node names in lexical order
            if tuple[0] < n:  # node value sort order
                edgeId = tuple[0]+'-'+n
            else:
                edgeId = n+'-'+tuple[0]
            edgeValues[edgeId] = tuple[1]
    sum = 0
    for edgeId in edgeValues:
        sum += edgeValues[edgeId]
    return sum

# ======== solution functions =====================================


def question1(s, t):
    """return True if an anagram of t is a substring of s."""
    # check each position of s for an anagram of t
    lenT = len(t)
    if lenT == 0:
        return True
    candidateStart = -1
    lastPossibleStart = len(s) - len(t)
    while candidateStart < lastPossibleStart:
        candidateStart += 1
        if anagramFound(s, t, candidateStart):
            return True
    return False


def question2FirstTry(a):
    aLength = len(a)
    if aLength <= 0:
        return ''

    # until we find a longer one, the first char will do
    longest = Palindrome(0,1)  # if no longer ones found, pick first char

    # now look for palindromes of length 2
    stillToExplore = LinkedList()
    for i in range(0,len(a)-2):
        if a[i] == a[i+1]:
            p = Palindrome(i,2)
            stillToExplore.insert(p)
            longest = p

    # look for palindromes of length 3
    for i in range(0,len(a)-2):
        if a[i] == a[i+2]:
            p = Palindrome(i,3)
            stillToExplore.insert(p)
            longest = p

    # keep looking for longer palindromes
    while stillToExplore.head:
        # iterate through list
        p = stillToExplore.head
        while p:
            if canGrow(p, aLength) and (a[p.start-1] == a[p.start + p.length]):
                p.start -= 1
                p.length += 2
                if longest.length < p.length:
                    longest = p
            else:
                stillToExplore.remove(p)
            p = p.next

    # now longest is last long Palindrome seen and no more to explore
    return a[longest.start:longest.start+longest.length]


def question2(a):
    aLength = len(a)
    l = aLength
    while l > 0:
        for start in range(0, aLength - (l-1)):
            if a[start:start+l:1] == a[start+l-1:None if (start-1)<0 else (start-1):-1]:
                return a[start:start+l:1]
        l -= 1
    return ''


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
            nmap[id1].addEdge(edge)
            nmap[id2].addEdge(edge)

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
    return adjacencyList(partitions[0])


# ========= test cases =============================================

# ========= question1 ========
assert question1('', '') == True
assert question1('', 'a') == False
assert question1('b', 'b') == True
assert question1('abc', 'b') == True
assert question1('abc', 'cb') == True
assert question1('abc', 'cab') == True
assert question1('abcbcbbbc', 'aca') == False

# ========= question2 ========

assert question2('') == ''
assert question2('a') == 'a'
assert question2('b') == 'b'
assert question2('abc') == 'a'
assert question2('abbc') == 'bb'
assert question2('abbbc') == 'bbb'
assert question2('abccb') == 'bccb'
assert question2('bccba') == 'bccb'
assert question2('abcdcb') == 'bcdcb'
assert question2('bcdcba') == 'bcdcb'
assert question2('abcdcdccdedccbb') == 'ccdedcc'
assert question2('abcdefe') == 'efe'

# ========= question3 ========

# g = {'A': [('B', 2)],
#  'B': [('A', 2), ('C', 5)],
#  'C': [('B', 5)]}
# mst = question3(g)
# assert sumEdges(mst) == 7

g = {
    'A': [('B', 3), ('F', 5), ('C', 2)],
    'B': [('A', 3), ('C', 4), ('D', 1)],
    'C': [('A', 2), ('B', 4), ('E', 1)],
    'D': [('B', 1), ('E', 5), ('F', 1)],
    'E': [('C', 1), ('D', 5), ('F', 1)],
    'F': [('E', 1), ('A', 5), ('D', 1)],
}
mst = question3(g)
assert sumEdges(mst) == 6

# ========= question4 ========

# ========= question5 ========
