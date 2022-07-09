# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 15:22:42 2021

@author: Mike
"""

def Process_without_memory(D = ["a","b","c","d","e"], 
                        mode = ["min_entropy","max_entropy","med_entropy"][2], 
                        num_traces=2,
                        settings={"med_ent_e_steps":5,
                                          "med_ent_n_transitions":5,
                                          "med_ent_max_trials":100}):
    import numpy as np
    import pandas as pd
    
    from simulation.alg2_initial_probabilities import GenerateInitialProb
    from simulation.alg3_transition_matrix_min_entropy import Generate_transition_matrix_min_ent
    from simulation.alg4_transition_matrix_max_entropy import Generate_transition_matrix_max_ent
    from simulation.alg5_transition_matrix_med_entropy import Generate_transition_matrix_med_ent
  
    #mode = ["min_entropy","max_entropy","med_entropy"][1]
    repetitions = num_traces

    #D = ["a","b","c","d","e"]
    D_abs = D.copy()
    D_abs.append("END")

    # Eventlog
    Theta = []
    
    if mode =="min_entropy":
        #initial probabilities
        P0 = GenerateInitialProb(D, p0_type="min_entropy")
        P = Generate_transition_matrix_min_ent(D, P0)
        P.index = D_abs
        
    if mode =="max_entropy":
        #initial probabilities
        P0 = GenerateInitialProb(D, p0_type="max_entropy")
        P = Generate_transition_matrix_max_ent(D)
        P.index = D_abs
        
    if mode =="med_entropy":
        #initial probabilities
        P0 = GenerateInitialProb(D, p0_type="med_entropy")
        P = Generate_transition_matrix_med_ent(D,
                                               #e_steps=settings["med_ent_e_steps"],
                                               n_tranitions=settings["med_ent_n_transitions"],
                                               limit_trials=settings["med_ent_max_trials"])
        P.index = D_abs
    
    # Transition matrices
    Phi = [P0, P]
    
        
    for trace in list(range(0,repetitions)):
            
        #placeholder for trace
        sigma = []
        
        #counter
        t=1
        
        #sample from initial distribution
        e_t = np.random.choice(D, #len(D), #
                               size=1, replace=False, p=P0)[0]
        
        #append first event to trace
        sigma.append(e_t)
        
        while e_t != D_abs[len(D_abs)-1]:
            t = t+1
        
            #get conditional probability (e_t'th row of P)
            p_t = P.loc[P.index==e_t]
            
            #sample event from P
            #e_t = np.random.choice(p_t.columns, size=1, replace=False, p=np.reshape(p_t.values,(len(D))))[0]
            
            e_t = np.random.choice(D_abs, size=1, replace=False, p=p_t.values[0])[0]
            
            sigma.append(e_t)
        
        #print("trace:",sigma)

        Theta.append(sigma)
    #Evaluate number of traces generated
    #print("Number of cases in Theta:",str(len(Theta)),"=> specified:",str(repetitions))
    return Theta, Phi

#Theta, Phi = Process_without_memory(D = ["a","b","c","d","e"], 
#                        mode = ["min_entropy","max_entropy","med_entropy"][2], 
#                        num_traces=10)