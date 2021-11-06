from termcolor import colored

def dfs(state, adj):
	vis = set()
	vis.add(state)
	st = [state]
	while len(st)>0:
		top = st.pop()

		if top not in adj:
			continue

		for u in adj[top]:
			if u not in vis:
				vis.add(u)
				st.append(u)
	return vis

def epsilon_closure_generator(states : set, transitions : list) -> dict:
	adj = {}

	for t in transitions:
		if len(t) == 2:
			current = t[0]
			nextstate = t[1]
			if current not in adj:
				adj[current] = []
			adj[current].append(nextstate)

	epsilon_closure_set = {}

	for state in states:
		epsilon_closure_set[state] = dfs(state, adj)

	return epsilon_closure_set

def closure_set_transition_by_state(state, symbol, transitions, epsilon_closure_set):
	ret = set()
	for t in transitions:
		if len(t) == 3 and t[0] in epsilon_closure_set[state] and t[1] == symbol:
			ret = ret | epsilon_closure_set[t[2]]
	return ret

def DFA_generator(start_state, states, symbols, transitions, epsilon_closure_set):
	st = [epsilon_closure_set[start_state]]
	vis = set()
	vis.add(frozenset(epsilon_closure_set[start_state]))
	ret = []

	while len(st) > 0:
		top = st.pop()

		for symbol in symbols:
			next_set = set()
			for state in top:
				next_set = next_set | closure_set_transition_by_state(state, symbol, transitions, epsilon_closure_set)
			next_set_frozen = frozenset(next_set)
			if len(next_set_frozen) == 0:
				continue
			if next_set_frozen not in vis:
				vis.add(next_set_frozen)
				st.append(next_set_frozen)
				ret.append([top, symbol, next_set])

	return ret

def output_format(transition : list, final_states : list, epsilon_closure_start : set):
	state1 = str(transition[0])
	if transition[0] == epsilon_closure_start and any(f in transitions[0] for f in final_states):
		state1 = colored(state1, 'green')
	elif transition[0] == epsilon_closure_start:
		state1 = colored(state1, 'yellow')
	elif any(f in transitions[0] for f in final_states):
		state1 = colored(state1, 'red')

	state2 = str(transition[2])
	if transition[2] == epsilon_closure_start and any(f in transitions[2] for f in final_states):
		state2 = colored(state2, 'green')
	elif transition[2] == epsilon_closure_start:
		state2 = colored(state2, 'yellow')
	elif any(f in transitions[2] for f in final_states):
		state2 = colored(state2, 'red')

	print(state1, '---', colored(transition[1], 'cyan') , '--- >', state2)


if __name__ == "__main__":
	print('Hello, this is a NFA-to-DFA converter.')
	start_state = input('Please enter the start state: ')
	final_states = input('Please enter the final states (seperated by white space): ').split()

	total_transition = int(input('Please enter the number of transition function: '))

	transitions = []
	symbols = set()
	print('For each of the following line please input the transition function in the form:')
	print('[state1] [symbol] [state2]')
	print('There are',colored('spaces', 'red'), 'between the symbols')
	print('You could omit the symbol to indicate epsilon transition.')

	for i in range(total_transition):
		transitions.append(input().split())

	states = set()

	for t in transitions:
		if len(t) == 2:
			states.add(t[0])
			states.add(t[1])
		else:
			states.add(t[0])
			states.add(t[2])
			symbols.add(t[1])

	epsilon_closure = epsilon_closure_generator(states, transitions)

	DFA = DFA_generator(start_state, states, symbols, transitions, epsilon_closure)

	print('This is the DFA: ')
	for t in DFA:
		output_format(t, final_states, epsilon_closure[start_state])

