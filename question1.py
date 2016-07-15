"""Question 1: Given two strings s and t, determine whether some anagram
of t is a substring of s. For example: if s = 'udacity' and t = 'ad',
then the function returns True. Your function definition should look
like: 'question1(s, t)', and return a boolean True or False."""

"""Complexity is a function of both len s and len t.  Call these n and m.
The main function question1 has a main loop that executes in the worst
case n times as it iterates through positions of s.  Inside this loop, the
function 'anagramFound' iterates m times as it checks for each letter in t,
but it also calls 'if s[p] in bag' and 'bag.remove(s[p])', which are both
O(m).  So the inner loop executes in the worst case m * 2m.  The overall
complexity is O(nm^2).  It is worth noting that the algorithm returns False
immediately if m > n and any optimization should consider the common range
of sizes for each input.

Space complexity is O(m) since each call of anagramFound allocates and 
frees a list of size m.  This memory management could be eliminated by
reusing a bag data structure that allowed us to keep track
which letters had been removed.
"""

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

def test(s, t, expect):
	print('{}, {} expect {}, actual {}'.format(s, t, expect, question1(s, t)))

test('', '', True)
test('', 'a', False)
test('b', 'b', True)
test('abc', 'b', True)
test('abc', 'cb', True)
test('abc', 'cab', True)
test('abcbcbbbc', 'aca', False)
