from collections import defaultdict

from search_py3.search import GraphProblem
from search_py3.search import Graph
from search_py3.search import breadth_first_search

WORDS = set(i.lower().strip() for i in open('./search_py3/words2.txt'))

class WordLadderProblem(GraphProblem):
	"""
	Class that implements Word Ladder Problem as Graph Problem

	Args:
		- start_word : str
		- goal_word : str
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
	def __init__(self, start_word, goal_word, WORDS):
		try:
			self.check(start_word, goal_word, WORDS)
			self.preprocess(WORDS)
			super().__init__(start_word, goal_word, self.word_graph)

		except AssertionError as err: print(err)

	def solve(self):
		return breadth_first_search(self).solution()

	def preprocess(self, WORDS):
		self.word_dict = self.build_dict(WORDS)
		self.word_graph = self.build_graph(self.word_dict)
		return self.word_graph

	def build_dict(self, WORDS):
		word_dict = defaultdict(list)
		for word in WORDS:
			if len(word) == self.length: # just checks words of that length
				for i in range(self.length):
					word_dict[ word[:i] + "*" + word[i+1:] ].append(word)
					# e.g. {CO*D : [COLD, CORD, ...], ...}
		return word_dict

	def build_graph(self, word_dict):
		word_graph = defaultdict(dict)
		for intermediate_word in word_dict.keys():
			for word1 in word_dict[intermediate_word]:
				for word2 in word_dict[intermediate_word]:
					if word1 != word2:
						word_graph[word1][word2] = 1
						# connect 1 word to every other word in a dictionary
						# {'lilt': {'kilt': 1, 'gilt': 1, 'jilt': 1, ...}, ...}
		return Graph(word_graph, directed=False)

	def check(self, start_word, goal_word, WORDS):
		assert len(start_word) == len(goal_word), "Length of start and end words must be the same!"
		assert self.is_valid_word(start_word)
		assert self.is_valid_word(goal_word)

		self.length = len(start_word)
		print(f"Valid Problem! Word length: {self.length}")

	def is_valid_word(self, word):
		return word in WORDS

if __name__ == "__main__":
	test_cases = [
		("cars", "cats"),
		("cold", "warm"),
		("best", "math"),
	]

	for start_word, goal_word in test_cases:
		problem = WordLadderProblem(start_word, goal_word, WORDS)
		solution = problem.solve()
		print(f"{start_word} -> {solution} -> {goal_word}")

