import pdb
from csp import *
from random import shuffle

def solve_semi_magic(algorithm=backtracking_search, **args):
	""" From CSP class in csp.py
		vars 				A list of variables; each is atomic (e.g. int or string).
		domains 		A dict of {var:[possible_value, ...]} entries.
		neighbors 	A dict of {var:[var,...]} that for each variable lists
									the other variables that participate in constraints.
		constraints A function f(A, a, B, b) that returns true if neighbors
									A, B satisfy the constraint when they have values A=a, B=b
	"""

	# Use the variable names in the figure
	csp_vars = ['V%d'%d for d in range(1,10)]

	#########################################
	# Fill in these definitions

	csp_domains = {x: [1, 2, 3] for x in csp_vars}
	csp_neighbors = {
		'V1': ['V2','V3','V4','V7','V5','V9'],
		'V2': ['V1','V3','V5','V8'],
		'V3': ['V1','V2','V6','V9'],
		'V4': ['V1','V7','V5','V6'],
		'V5': ['V1','V2','V4','V6','V8','V9'],
		'V6': ['V4','V5','V3','V9'],
		'V7': ['V1','V4','V8','V9'],
		'V8': ['V7','V2','V5','V9'],
		'V9': ['V1','V5','V3','V6','V7','V8'],
	}

	def csp_constraints(A, a, B, b):
		return (a != b)

		#########################################

	# define the CSP instance
	csp = CSP(csp_vars, csp_domains, csp_neighbors,
	          csp_constraints)

	# run the specified algorithm to get an answer (or None)
	ans = algorithm(csp, **args)

	print('number of assignments:', csp.nassigns)
	assign = csp.infer_assignment()
	if assign:
		for x in sorted(assign.items()):
			print(x)

	print("__")
	return csp

def test():
	print('Testing the following:')

	result = {}

	BTS = 'Backtracking Search'
	MRV = 'Minimum Remaining Values Heuristic'
	LCV = 'Least Constraining Values Heuristic'
	BTFC = 'Backtracking Search with Forward Checking'
	BTAC = 'Backtracking Search with Arc Consistency'

	test = [BTS, MRV, LCV, BTFC, BTAC]

	print('Testing:')
	for i in range(len(test)):
		print(f'{i+1}. {test[i]}')
		if test[i] == BTS: result[BTS] = solve_semi_magic(algorithm=backtracking_search).nassigns
		elif test[i] == MRV: result[MRV] = solve_semi_magic(select_unassigned_variable=mrv).nassigns
		elif test[i] == LCV: result[LCV] = solve_semi_magic(order_domain_values=lcv).nassigns
		elif test[i] == BTFC: result[BTFC] = solve_semi_magic(inference=forward_checking).nassigns
		elif test[i] == BTAC: result[BTAC] = solve_semi_magic(inference=mac).nassigns
		else: "Test setting does not exist"

	print(f'Result: {result}')

if __name__ == '__main__':
	test()
	print()
	print('Most algorithm finds the answer with the minimum amount of assignments possible, i.e: 9 because the problem is very simple.')
	print('However, Minimum Remaining Values Heuristic can sometimes use up a lot of assignments, i.e: 33 assignments.')
	print('MRV makes the solver explores branches that do not result in solution, causing backtracking and additional assignments.')
