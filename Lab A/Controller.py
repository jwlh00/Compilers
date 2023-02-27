from ToPostfix import *
from Thompson import *
from Graph import *

def fromRegexToAFN(regex):
    postfix = getPostfix(regex)
    # print(postfix)
    nfa = postfix_to_nfa(postfix)
    dot = graph_nfa(nfa)
    dot.render('nfa', format='png')


