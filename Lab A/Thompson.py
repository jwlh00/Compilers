class State:
    def __init__(self, name=None, label=None):
        self.name = name
        self.transitions = {}
        self.label = label
        self.epsilonTransitions = set()

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

def postfix_to_nfa(postfix):
    stack = []
    for c in postfix:
        if c == '.':
            #For concatenation
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept.epsilonTransitions.add(nfa2.start)
            stack.append(NFA(nfa1.start, nfa2.accept))
        elif c == '|':
            #For alternation
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            accept = State()
            start.epsilonTransitions.update([nfa1.start, nfa2.start])
            nfa1.accept.epsilonTransitions.add(accept)
            nfa2.accept.epsilonTransitions.add(accept)
            stack.append(NFA(start, accept))
        elif c == '*':
            #For Kleene star
            nfa = stack.pop()
            start = State()
            accept = State()
            start.epsilonTransitions.update([nfa.start, accept])
            nfa.accept.epsilonTransitions.update([nfa.start, accept])
            stack.append(NFA(start, accept))
        elif c == '+':
            #For one-or-more
            nfa = stack.pop()
            start = State()
            accept = State()
            start.epsilonTransitions.add(nfa.start)
            nfa.accept.epsilonTransitions.update([nfa.start, accept])
            stack.append(NFA(start, accept))
        elif c == '?':
            #For zero-or-one
            nfa = stack.pop()
            start = State()
            accept = State()
            start.epsilonTransitions.add(nfa.start)
            start.epsilonTransitions.add(accept)
            nfa.accept.epsilonTransitions.add(accept)
            stack.append(NFA(start, accept))
        else:
            #For normal symbols
            accept = State()
            start = State()
            start.transitions[c] = accept
            stack.append(NFA(start, accept))
    return stack.pop() 


