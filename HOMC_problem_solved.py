# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:25:06 2022

@author: Mike
"""

# from pomegranate import DiscreteDistribution, ConditionalProbabilityTable, MarkovChain

# p0 = DiscreteDistribution({'A': 0.10, 'C': 0.40, 'G': 0.40, 'END': 0.10})

# p1 = ConditionalProbabilityTable([['A', 'A', 0.10],
#                                     ['A', 'C', 0.50],
#                                     ['A', 'G', 0.30],
#                                     ['A', 'END', 0.10],
#                                     ['C', 'A', 0.10],
#                                     ['C', 'C', 0.40],
#                                     ['C', 'END', 0.40],
#                                     ['C', 'G', 0.10],
#                                     ['G', 'A', 0.05],
#                                     ['G', 'C', 0.45],
#                                     ['G', 'G', 0.45],
#                                     ['G', 'END', 0.05],
#                                     ['END', 'END', 0.20],
#                                     ['END', 'END', 0.30],
#                                     ['END', 'END', 0.30],
#                                     ['END', 'END', 0.20]], [p0])

# HOMC = MarkovChain([p0, p1])

# HOMC.sample(30)

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

# ['A', 'A', 0.10],
# ['A', 'C', 0.50],
# ['A', 'G', 0.30],
# ['A', 'END', 0.10],
# ['C', 'A', 0.10],
# ['C', 'C', 0.40],
# ['C', 'END', 0.40],
# ['C', 'G', 0.10],
# ['G', 'A', 0.05],
# ['G', 'C', 0.45],
# ['G', 'G', 0.45],
# ['G', 'END', 0.05],
# ['END', 'END', 0.20],
# ['END', 'END', 0.30],
# ['END', 'END', 0.30],
# ['END', 'END', 0.20]



"""
Should probabilities or rows reflect the absorption nature?

    Solution A: drop rows with sequences that are not possible
        - Faster
        - Illustrates reality
        
        - does not give a balanced matrix (not the cartesian product anymore)

    Solution B: change probability to 0 for paths that are not possible
        - prone to error
        
"""



""" 
generate expected format for conditional probability table
"""

from simulation.homc_helpers import create_homc

states = ["A","B","C", "D","E"]

h0 = {'A': 1.00, 
      'B': 0.00, 
      'C': 0.00, 
      'D': 0.00,
      'E': 0.00}


HOMC = create_homc(states, h0, h=4)



print(HOMC.sample(30))

