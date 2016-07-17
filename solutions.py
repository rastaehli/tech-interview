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

# ======== solution functions =====================================


def question1(s, t):
    """return True if an anagram of t is a substring of s."""
    # check each position of s for an anagram of t
    lenT = len(t)
    if lenT == 0:
        return True
    candidateStart = -1
    lastPossibleStart = len(s) - len(t)
    # print('candidateStart {} < lastPossibleStart {}'.format(candidateStart, lastPossibleStart))
    while candidateStart < lastPossibleStart:
        candidateStart += 1
        if anagramFound(s, t, candidateStart):
            return True
    return False


def question2(a):
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
                # print(p.start, p.length)
                if longest.length < p.length:
                    longest = p
            else:
                stillToExplore.remove(p)
            p = p.next

    # now longest is last long Palindrome seen and no more to explore
    # print(longest.start, longest.length)
    return a[longest.start:longest.start+longest.length]


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


# ========= test cases =============================================

# ========= question1 ========
print("question1('', '')")
print("expect: True")
print("question1('', '')")
print("expect: True")
print("question1('', 'a')")
print("expect: False")
print("question1('b', 'b')")
print("expect: True")
print("question1('abc', 'b')")
print("expect: True")
print("question1('abc', 'cb')")
print("expect: True")
print("question1('abc', 'cab')")
print("expect: True")
print("question1('abcbcbbbc', 'aca')")
print("expect: False")

# ========= question2 ========

print("question2('')")
print("expect: ''")
print("question2('a')")
print("expect: 'a'")
print("question2('b')")
print("expect: 'b'")
print("question2('abc')")
print("expect: 'a'")
print("question2('abbc')")
print("expect: 'bb'")
print("question2('abbbc')")
print("expect: 'bbb'")
print("question2('abccb')")
print("expect: 'bccb'")
print("question2('bccba')")
print("expect: 'bccb'")
print("question2('abcdcb')")
print("expect: 'bcdcb'")
print("question2('bcdcba')")
print("expect: 'bcdcb'")
print("question2('abcdcdccdedccbb')")
print("expect: 'ccdedcc'")
print("question2('abcdefe')")
print("expect: 'efe'")

# ========= question3 ========

def test(g, expect):
    print(g)
    print('expect {}, actual {}'.format(expect, question3(g).edgesSum()))

print("g = {'A': [('B', 2)],")
print(" 'B': [('A', 2), ('C', 5)],")
print(" 'C': [('B', 5)]}")
print("question3(g).edgesSum()")
print("expect: 7")

print("g = {")
print("    'A': [('B', 3), ('F', 5), ('C', 2)],")
print("    'B': [('A', 3), ('C', 4), ('D', 1)],")
print("    'C': [('A', 2), ('B', 4), ('E', 1)],")
print("    'D': [('B', 1), ('E', 5), ('F', 1)],")
print("    'E': [('C', 1), ('D', 5), ('F', 1)],")
print("    'F': [('E', 1), ('A', 5), ('D', 1)],")
print("}")
print("question3(g).edgesSum()")
print("expect: 6")

# ========= question4 ========

# ========= question5 ========
