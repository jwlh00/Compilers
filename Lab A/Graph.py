from graphviz import Digraph

def graph_nfa(automata):
    g = Digraph()
    epsilon = 'ε'

    # Add the states
    states = {}
    for i, state in enumerate(get_nfa_states(automata.start)):
        statestring = f'q{i}'
        if state in get_nfa_accept_states(automata.start):
            g.node(statestring, shape='doublecircle')
        else:
            g.node(statestring, shape='circle')
        if state == automata.start:
            g.node(statestring, shape='house')
        states[state] = statestring

    # Add the transitions
    transitions = get_nfa_transitions(automata.start)
    for state, symbols in transitions.items():
        for symbol, targets in symbols.items():
            for target in targets:
                if symbol == epsilon:
                    g.edge(states[state], states[target], label=epsilon)
                else:
                    g.edge(states[state], states[target], label=symbol)

    return g


def get_nfa_states(start):
    """
    Returns a set of all states in the NFA reachable from the start state.
    """
    states = set()
    queue = [start]
    while queue:
        state = queue.pop()
        if state in states:
            continue
        states.add(state)
        for target in state.transitions.values():
            queue.append(target)
        for target in state.epsilonTransitions:
            queue.append(target)
    return states


def get_nfa_accept_states(start):
    """
    Returns a set of all accept states in the NFA reachable from the start state.
    """
    states = set()
    queue = [start]
    while queue:
        state = queue.pop()
        if state in states:
            continue
        states.add(state)
        if state.label:
            continue
        for target in state.transitions.values():
            queue.append(target)
        for target in state.epsilonTransitions:
            queue.append(target)
    return states


def get_nfa_transitions(start):
    """
    Returns a dictionary of all transitions in the NFA reachable from the start state.
    The dictionary maps a state to a dictionary of transitions, where each transition maps
    a symbol to a set of states that it transitions to.
    """
    epsilon = 'ε'
    transitions = {}
    states = set()
    queue = [start]
    while queue:
        state = queue.pop()
        if state in states:
            continue
        states.add(state)
        for symbol, target in state.transitions.items():
            if state not in transitions:
                transitions[state] = {}
            if symbol not in transitions[state]:
                transitions[state][symbol] = set()
            transitions[state][symbol].add(target)
            queue.append(target)
        for target in state.epsilonTransitions:
            if state not in transitions:
                transitions[state] = {}
            if epsilon not in transitions[state]:
                transitions[state][epsilon] = set()
            transitions[state][epsilon].add(target)
            queue.append(target)
    return transitions