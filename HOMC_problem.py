# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:25:06 2022

@author: Mike
"""

from pomegranate import DiscreteDistribution, ConditionalProbabilityTable, MarkovChain

p0 = DiscreteDistribution({'A': 0.10, 'C': 0.40, 'G': 0.40, 'END': 0.10})

p1 = ConditionalProbabilityTable([['A', 'A', 0.10],
                                    ['A', 'C', 0.50],
                                    ['A', 'G', 0.30],
                                    ['A', 'END', 0.10],
                                    ['C', 'A', 0.10],
                                    ['C', 'C', 0.40],
                                    ['C', 'END', 0.40],
                                    ['C', 'G', 0.10],
                                    ['G', 'A', 0.05],
                                    ['G', 'C', 0.45],
                                    ['G', 'G', 0.45],
                                    ['G', 'END', 0.05],
                                    ['END', 'END', 0.20],
                                    ['END', 'END', 0.30],
                                    ['END', 'END', 0.30],
                                    ['END', 'END', 0.20]], [p0])

HOMC = MarkovChain([p0, p1])

HOMC.sample(30)

"""
How do I generate the p-table automatically?

- each of the branching possibilities from a prior state needs to sum to 0
- once "END" has been introduced, it should only lead to "END"

- possiblities in the transition matrices has to be according to 3 different
  entropy-related settings: min, medium and max entropy

"""


"""

IS it faster or easier to use pomegranate?

    - Data-structure could be easier to create than a matrix, using pandas
    
    - Having mentioned it as a possiblity in the literature review,
      it might be good to use pomegranate as a dependency
      
          - which could extend the simulation model, such that it could be 
            calibrated with existing data (e.g. as in paper 4)

"""

import numpy as np
import pandas as pd


states = ["A","B","C","E"]
h = 2

"""
Generate transition possibilities
"""

def gen_t1_t2_states(states, h=2):
    from simulation.simulation_helpers import flatten
    
    t1 = []
    t2 = []

    for state in states:
        """
        T1
        """
        
        l = [state]*len(states)
        
        t1.append(l)
        t1 = flatten(t1)

        for i in range(0,h-1):
            """
            T2
            """
                    
            if state == "E":
                t2.append(["E"]*len(states))       
                t2 = flatten(t2)
            else:
                t2.append(states)        
                t2 = flatten(t2)
    return t1, t2

t1, t2 = gen_t1_t2_states(states, h=2)
print(t1)
print(t2)


"""
Generate probabilities
"""        

def gen_p(states):
    from simulation.simulation_helpers import flatten
    
    p = []
    for i in states:
        #get list of probabilities for each state
        vec = np.random.random(len(states))
        
        #normalize it
        vec = np.round(vec/np.sum(vec), decimals=5)
        
        p.append(vec.tolist())
        
    p = flatten(p)
    # print(p) 
    return p


###############################################################################



"""
Collect results into a nested list in correct format:
"""

def gen_condprob(t1,t2,p):
    import pandas as pd
    table = pd.DataFrame({"t1":t1,
                          "t2":t2,
                          "p":p})
    table_t = table.T

    condprob = []

    for i in range(0,len(table)):
        row = table_t[i].values.tolist()
        condprob.append(row)

    print(condprob)
    return condprob



###############################################################################

"""
Generate unconditional probabilities
"""
def gen_uncondprob(states):
    import numpy as np

    vec = np.random.random(len(states))
    vec = np.round(vec/np.sum(vec), decimals=5)
    t0p = vec.tolist()

    uncondprob = {}

    for i in range(0,len(states)):
        state = states[i]
        prob = t0p[i]
        uncondprob.update({state:prob})

    print(uncondprob)
    
    return uncondprob

###############################################################################

"""
Test functionality
"""

p = gen_p(states)

t1, t2 = gen_t1_t2_states(states, h=2)

condprob = gen_condprob(t1, t2, p)

uncondprob = gen_uncondprob(states)

###############################################################################

"""
Test functionality
"""


from pomegranate import DiscreteDistribution, ConditionalProbabilityTable, MarkovChain

p0 = DiscreteDistribution(uncondprob)

p1 = ConditionalProbabilityTable(condprob, [p0])

HOMC = MarkovChain([p0, p1])

HOMC.sample(3)

"""
###############################################################################
"""

