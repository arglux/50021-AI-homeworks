from collections import defaultdict

from search_py3.search import GraphProblem
from search_py3.search import Graph
from search_py3.search import breadth_first_search

WORDS = set(i.lower().strip() for i in open('./search_py3/words2.txt'))

class WordLadderProblem(GraphProblem):
	"""
	Class that implements Word Ladder Problem as Graph Problem

	Args:
		- startWord : str
		- goalWord : str
		- WORDS : set (set of all posible words)

	The main work that this class does is generating an Undirected Graph of how words are connected
	e.g. {'lilt': {'kilt': 1, 'gilt': 1, 'jilt': 1, ...}, ...}
	Afterwhich, BFS is run on the graph to give the solution.

	This building of Undirected Graph (preprocess) is done in following manner:
		1. Checks all assumptions (equal length, start and end words exist in WORDS set, etc)
		2. Given all words with this known length, generate all dictionary of all intermediate words
				e.g. {CO*D : [COLD, CORD, ...], ...}
		3. Finally, simply build the dictionary to pass into UndirectedGraph's constructor
	"""
	def __init__(self, startWord, goalWord, WORDS):
		try:
			self.check(startWord, goalWord, WORDS)
			self.preprocess(WORDS)
			super().__init__(startWord, goalWord, self.wordGraph)

		except AssertionError as err: print(err)

	def solve(self):
		return breadth_first_search(self).solution()

	def preprocess(self, WORDS):
		self.wordDict = self.buildDict(WORDS)
		self.wordGraph = self.buildGraph(self.wordDict)
		return self.wordGraph

	def buildDict(self, WORDS):
		wordDict = defaultdict(list)
		for word in WORDS:
			if len(word) == self.length: # just checks words of that length
				for i in range(self.length):
					wordDict[ word[:i] + "*" + word[i+1:] ].append(word)
					# e.g. {CO*D : [COLD, CORD, ...], ...}
		return wordDict

	def buildGraph(self, wordDict):
		wordGraph = defaultdict(dict)
		for intermediateWord in wordDict.keys():
			for word1 in wordDict[intermediateWord]:
				for word2 in wordDict[intermediateWord]:
					if word1 != word2:
						wordGraph[word1][word2] = 1
						# connect 1 word to every other word in a dictionary
						# {'lilt': {'kilt': 1, 'gilt': 1, 'jilt': 1, ...}, ...}
		return Graph(wordGraph, directed=False)

	def check(self, startWord, goalWord, WORDS):
		assert len(startWord) == len(goalWord), "Length of start and end words must be the same!"
		assert self.is_valid_word(startWord)
		assert self.is_valid_word(goalWord)

		self.length = len(startWord)
		print(f"Valid Problem! Word length: {self.length}")

	def is_valid_word(self, word):
		return word in WORDS

if __name__ == "__main__":
	test_cases = [
		("cars", "cats"),
		("cold", "warm"),
		("best", "math"),
	]

	for startWord, goalWord in test_cases:
		problem = WordLadderProblem(startWord, goalWord, WORDS)
		solution = problem.solve()
		print(solution)

