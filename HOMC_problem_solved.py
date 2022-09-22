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

['A', 'A', 0.10],
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
['END', 'END', 0.20]


import numpy as np
import pandas as pd
from simulation.simulation_helpers import flatten

states = ["A","B"]
h = 3


############ Alternative approach: self-adapting


def generate_parent(states, h=3):
    from simulation.simulation_helpers import flatten
    t_i = []
    
    for state in states:
        #calculate the expected length of first row
        n = int((len(states)**h)/len(states))
        
        #add n elements
        t_i.append([state]*n)
    t_i = flatten(t_i)
    return t_i

parent = generate_parent(states, h=3)
print(parent)




def generate_child(parent, states):
    from simulation.simulation_helpers import flatten
    # if the state repeats itself more than len(statespace) times,
    # it means that this is not the last column, and the pattern therefore
    # needs to be determined by a formula
    # 

    #find number of repetitions in parent vector (reps of first state)
    number_of_repetitions = len([val for val in parent if val == states[0]])

    #repeat each state this number of times:
    states_by_repetitions = int(number_of_repetitions/len(states))
    n_rep = states_by_repetitions

    # repeat the repetitions this many times
    n_rep_2 = int(len(parent)/(n_rep*len(states)))
    
    #result vector placeholder
    l = []
    
    for rep in range(0, n_rep_2):
        
        for state in states:
            
            l.append([state]*n_rep)
            
    child = flatten(l)
    return child



parent = generate_parent(states, h=4)

child = generate_child(parent, states)


child2 = generate_child(child, states)





# def create_child(parent, states):
    
#     unique = list(dict.fromkeys(parent))
    
#     n_states = len(states)
    
#     for state in states:
#         parent_i = [val for val in parent if val == state]
#         n_parent = len(parent_i)

#         n_repetitions = int(n_parent/len(states))
    
#     return child

# h = 3



# r1 = int((len(states)**h)/len(states))


# target = int((len(states)**h))



# def generate_child(states, h_i=2):
    
#     from simulation.simulation_helpers import flatten
#     t_i = []
    
#     for state in states:
#         for i in range(0,h_i-1):
                    
#             if state == "E":
#                 t_i.append(["E"]*len(states))       
#                 t_i = flatten(t_i)
#             else:
#                 t_i.append(states)        
#                 t_i = flatten(t_i)
#     return t_i












#cartesian product:


def cartesian_product(a,b):
    import itertools

    c = list(itertools.product(a, b))
    return c


def combine_to_list(c):
    from simulation.simulation_helpers import flatten
    
    # combine the letters into one item
    newlist = []
    
    for i in range(0,len(c)):
        combination = flatten(c[i])
        newlist.append(combination)
            
    return newlist

def modify_to_absorption(c):
    """
    iterate over each line, and if E occurs at any point
    """
    newlist = []
    
    return newlist

"""
Should probabilities or rows reflect the absorption nature?

    Solution A: drop rows with sequences that are not possible
        - Faster
        - Illustrates reality
        
        - does not give a balanced matrix (not the cartesian product anymore)

    Solution B: change probability to 0 for paths that are not possible
        - prone to error
        
"""


def modify_rules(parent, states):
    import numpy as np
    #append probabilities to each row in the condition table
    condprob=[]
        
    #for each parent state
    for parentstate in states:
        
        #subset all rows starting with parent state i
        subset = [row for row in parent if row[0] == parentstate]

        """# manipulate the list """
        
        #All rows, starting with E, should lead only to E
        #If a sequence has E at any point, every subsequent entry becomes E
        
        new_subset = []
        
        for row in subset:
            
            #make a new row, based on rules
            newrow=[]
            
            #flag-variable
            e_observed = False
            
            for idx in range(0,len(row)):
                
                
                # if e is observed in current timestep, set flag to true
                if row[idx] == "E":
                    e_observed = True
                
                # 
                if e_observed == True:
                    value = "E"
                else:
                    value = row[idx]
                
                #append new value, based on above logic
                newrow.append(value)
                
                                
            #append new modified row
            new_subset.append(newrow)

        """
        #get list of probabilities for each state
        vec = np.random.random(len(subset))
        
        #normalize it
        vec = np.round(vec/np.sum(vec), decimals=5)
        vec = vec.tolist()
        
        for i in range(0,len(subset)):
            #get the probability
            p = vec[i]
            
            #append it to row i in subset
            subset[i].append(p)
            
        #"""
        
        #append to final list
        condprob = condprob + new_subset
    
    return condprob


def generate_condprob(parent, states):
    import numpy as np
    #append probabilities to each row in the condition table
    condprob=[]
        
    #for each parent state
    for parentstate in states:
        
        #subset all rows starting with parent state i
        subset = [row for row in parent if row[0] == parentstate]

        """# manipulate the list """
        
        #All rows, starting with E, should lead only to E
        #If a sequence has E at any point, every subsequent entry becomes E
        
        #"""
        #get list of probabilities for each state
        vec = np.random.random(len(subset))
        
        #normalize it
        vec = np.round(vec/np.sum(vec), decimals=5)
        vec = vec.tolist()
        
        for i in range(0,len(subset)):
            #get the probability
            p = vec[i]
            
            #append it to row i in subset
            subset[i].append(p)
            
        #"""
        #append to final list
        condprob = condprob + subset
    
    return condprob

""" 
generate expected format for conditional probability table
"""

states = ["A","B","C","E"]

h = 3

#for each link
c = cartesian_product(states, states)
d = combine_to_list(c)

e = cartesian_product(c, d)
f = combine_to_list(e)

#final steps
g = modify_rules(f, states)
p1_input = generate_condprob(g, states)





"""
Test functionality with pomegranate
"""


from pomegranate import DiscreteDistribution, ConditionalProbabilityTable, MarkovChain

p0 = DiscreteDistribution({'A': 0.10, 'B': 0.40, 'C': 0.40, 'E': 0.10})

p1 = ConditionalProbabilityTable(p1_input, [p0])

HOMC = MarkovChain([p0, p1])

HOMC.sample(30)

