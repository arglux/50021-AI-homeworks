from collections import defaultdict

from search_py3.search import Node
from search_py3.search import Problem
from search_py3.search import breadth_first_search

class Flight:
	def __init__(self, start_city, start_time, end_city, end_time):
		self.start_city = start_city
		self.start_time = start_time
		self.end_city = end_city
		self.end_time = end_time

	def matches(self, start_city, start_time):
		"""
		Part 2. Given the query start_city & start_time, see if this flight 'match'
		"""
		return (self.start_city == start_city) and (self.start_time >= start_time)

	def __str__(self):
		return str((self.start_city, self.start_time))+' -> '+ str((self.end_city, self.end_time))

	__repr__ = __str__

class FlightItineraryProblem(Problem):
	def __init__(self, flight, flightDB):
		self.flightDB = flightDB
		self.initial_state = (flight.start_city, flight.start_time)
		self.goal_state = (flight.end_city, flight.end_time)
		super().__init__(initial=self.initial_state, goal=self.goal_state)

	def actions(self, state):
		start_city = state[0]
		start_time = state[1]
		flight_list = [flight for flight in flightDB if flight.matches(start_city, start_time)]
		return flight_list

	def result(self, state, action):
		next_state = (action.end_city, action.end_time)
		return next_state

	def goal_test(self, state):
		current_city = state[0]
		current_time = state[1]
		end_city = self.goal[0]
		deadline = self.goal[1]
		return (current_city == end_city) and (current_time <= deadline)

	def solve(self):
		paths = breadth_first_search(self).path()
		return [itinerary.action for itinerary in paths if itinerary.action is not None]

	def find_itinerary(self):
		"""
		Part 3. Returns an itinerary (list of Flights) to reach end dest in time from a starting pt.
		"""
		try:
			return self.solve()
		except AttributeError as err: return f"No solution found. {err}"

	def find_shortest_itinerary(self, deadline=99):
		end_city = self.goal[0]
		for d in range(deadline):
			self.goal = (end_city, d)
			try: return(self.solve())
			except: continue

flightDB = [
		Flight('Rome', 1, 'Paris', 4),
		Flight('Rome', 3, 'Madrid', 5),
		Flight('Rome', 5, 'Istanbul', 10),
		Flight('Paris', 2, 'London', 4),
		Flight('Paris', 5, 'Oslo', 7),
		Flight('Paris', 5, 'Istanbul', 9),
		Flight('Madrid', 7, 'Rabat', 10),
		Flight('Madrid', 8, 'London', 10),
		Flight('Istanbul', 10, 'Constantinople', 10)
	]

if __name__ == "__main__":
	print("Part 1. Answer: Current city & current time")

	query = ('Rome', 3)
	print(f"Part 2. Testing: {flightDB[1]} matches {query} ? {flightDB[1].matches(*query)}")

	test_cases = [
		Flight('Rome', 1, 'London', 10),
		Flight('Rome', 1, 'Oslo', 10),
		Flight('Rome', 1, 'Istanbul', 10),
		Flight('Rome', 1, 'Indonesia', 10)
	]

	print("Part 3. Testing: find_itinerary()")
	for flight in test_cases:
		problem = FlightItineraryProblem(flight, flightDB)
		solution = problem.find_itinerary()
		print(solution)

	print("Part 4. Testing: find_shortest_itinerary()")
	problem = FlightItineraryProblem(Flight('Rome', 1, 'Istanbul', 10), flightDB)
	solution = problem.find_shortest_itinerary()
	print(solution)
