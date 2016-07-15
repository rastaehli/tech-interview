"""Question 2
Given a string a, find the longest palindromic substring contained in a. Your
function definition should look like question2(a), and return a string."""

"""complexity is a function of the length of a which we'll call n.  To setup
the linked list of candidate palindromes, this algorithm iterates through 
nearly all elements once to find doubles, then again to find palindromes of 
length three.  

In the worst case (all letters the same) the main loop begins
with a list of approximately 2n palindromes of length 2 and 3 and removes the 
outer four (2 that started as doubles and 2 that started as triples) each 
iteration until none are left: the number of palindromes visited in each
pass through the list is 2n + 2n-4 + 2n-8... or approximately n^2.  
Because the length of the largest palindrome grows by two characters each 
pass, it takes n/2 iterations before the algorithm terminates.  The
operations within the inner loop to test and grow/remove each palindrome
are constant time, so the complexity is 2n + n/2 * n^2, which in big-O
notation is O(n^3).

However, the average case is much better.  Suppose that the input was 
composed of common english language text and that the average case
longest palindrome was m, independent of the input text length n.  Then
the algorithm makes two passes through the full string to find the 2 and 
3 character palindromes and creates a list of perhaps n/10 palindromes found.
The size of the list shrinks rapidly with each pass as larger palindromes
are rare and the algorithm stops after m passes when no longer palindromes
are found.  The average case complexity is then approximately 2n + mn/10
or O(mn).  Since m is a constant, the complexity is O(n).

The additional space required is primarily for the linked list items, which
are small fixed size Palindrome objects.  The space complexity is O(n).
"""

def question2(a):
	"""return the longest palindromic substring of argument a.
	This solution uses divide and conquer: first observe that any empty
	or one character string is a palindrome.  Starting with these, look 
	for opportunities to extend each when they have matching characters at 
	either end.  Remember the longest found so far an also keep a list of 
	palindromes found that might still be extended."""
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

def canGrow(p, length):
	# True if index before and after are valid
	return (p.start > 0) and (p.start + p.length < length)

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

def test(a, expect):
	print('{} expect {}, actual {}'.format(a, expect, question2(a)))

test('', '')
test('a', 'a')
test('b', 'b')
test('abc', 'a')
test('abbc', 'bb')
test('abbbc', 'bbb')
test('abccb', 'bccb')
test('bccba', 'bccb')
test('abcdcb', 'bcdcb')
test('bcdcba', 'bcdcb')
test('abcdcdccdedccbb', 'ccdedcc')
test('abcdefe', 'efe')
