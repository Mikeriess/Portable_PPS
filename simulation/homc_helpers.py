# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 17:09:09 2022

@author: Mike
"""


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
            
            #for each step in the sequence
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