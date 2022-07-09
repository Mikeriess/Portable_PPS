#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 13:03:27 2021

@author: mikeriess
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 20:23:43 2021

@author: Mike
"""


def Generate_eventlog(SIM_SETTINGS):
    """
    

    Returns
    -------
    evlog_df : TYPE
        DESCRIPTION.

    """
    
    save_eventlog = SIM_SETTINGS["save_eventlog"]
    statespace = SIM_SETTINGS["statespace_size"]
    number_of_traces = SIM_SETTINGS["number_of_traces"]
    process_entropy = SIM_SETTINGS["process_entropy"]
    process_type = SIM_SETTINGS["process_type"]
    process_memory = SIM_SETTINGS["process_memory"]
    process_settings = SIM_SETTINGS["process_settings"]
    time_settings = SIM_SETTINGS["time_settings"]
    
    run = SIM_SETTINGS["run"]
    
    
    import pandas as pd
    import numpy as np
    
    from simulation.alg6_memoryless_process_generator import Process_without_memory
    from simulation.alg7_memory_process_generator import Process_with_memory
    from simulation.alg9_trace_durations import Generate_time_variables
    
    """
    Simulation pipeline:
    """
    
    # Generate an event-log
    if process_type == "memory":
        
        if process_memory != "min_entropy":
            Theta, Phi = Process_with_memory(D = statespace, 
                                    mode = process_entropy, 
                                    num_traces=number_of_traces, 
                                    K=process_memory,
                                    settings=process_settings)
        else:
            Theta, Phi = Process_without_memory(D = statespace, 
                                mode = process_entropy, 
                                num_traces=number_of_traces,
                                settings=process_settings)
    
    if process_type == "memoryless":
        Theta, Phi = Process_without_memory(D = statespace, 
                                mode = process_entropy, 
                                num_traces=number_of_traces,
                                settings=process_settings)
    
    # Generate time objects
    Y_container, Lambd, theta_time = Generate_time_variables(Theta = Theta,
                                                             D = statespace,
                                                             settings = time_settings)
    # get the max trace length
    max_trace_length = max(len(x) for x in Theta)
    
    #loop over all the traces
    for i in list(range(0,number_of_traces)):
        
        # get the activities
        trace = Theta[i]
        
        # remove "END" activity
        trace = list(filter(lambda a: a != "END", trace))
        
        # get the caseids
        caseids = [str(i)]*len(trace) #(max_trace_length-1)
        
        # generate timesteps
        timesteps = list(range(1,len(trace)+1))
        timesteps = [int(x) for x in timesteps]
            
        # generate a table
        trace = pd.DataFrame({"caseid":caseids,
                             "activity":trace,
                             "activity_no":timesteps,
                             "y_acc_sum":Y_container[i]["y_acc_sum"],
                             "X":Y_container[i]["X"],
                             "Y":Y_container[i]["Y"],
                             "z_t":Y_container[i]["z_t"],
                             "h_t":Y_container[i]["h_t"],
                             "b_t":Y_container[i]["b_t"],
                             "q_t":Y_container[i]["q_t"],
                             "s_t":Y_container[i]["s_t"],
                             "v_t":Y_container[i]["v_t"]})
        
        
        if i ==0:
            #make final table
            evlog_df = trace
    
        if i > 0:
            # append to the final table
            evlog_df = pd.concat((evlog_df,trace))
    
    # fix indexes
    evlog_df.index = list(range(0,len(evlog_df)))
    
    # convert starttime to a timestamp
    ###################################
    
    # year offset
    #year_offset = (60*60*24*365)*52
    year_offset = 0
    
    # 01/01/1970 is a thursday
    weekday_offset = 4 + year_offset
    
    #scaling from continuous units to preferred time unit
    time_conversion = (60*60*24)
    
    # copy the column
    
    """
    Generate arrival time
    """
    evlog_df['arrival_datetime'] = (evlog_df["X"] + weekday_offset)*time_conversion
    evlog_df['arrival_datetime'] = evlog_df['arrival_datetime'].astype('datetime64[s]') #%yyyy-%mm-%dd %hh:%mm:%ss
        
    """
    Generate activity start time
    """
    
    #evlog_df['start_datetime'] = ((evlog_df["Y"] - evlog_df["v_t"]) + weekday_offset)*time_conversion
    evlog_df['start_datetime'] = ((evlog_df["q_t"] + evlog_df["s_t"]) + weekday_offset)*time_conversion
    evlog_df['start_datetime'] = evlog_df['start_datetime'].astype('datetime64[s]')
    
    """
    Generate activity end time
    """
    
    evlog_df['end_datetime'] = (evlog_df["Y"] + weekday_offset)*time_conversion
    evlog_df['end_datetime'] = evlog_df['end_datetime'].astype('datetime64[s]')
 
    
    # control: get day of week of beginning work
    evlog_df['start_day'] = evlog_df['start_datetime'].dt.day_name()
    evlog_df['start_hour'] = evlog_df['start_datetime'].apply(lambda x: x.hour)
    
    if save_eventlog == True:
        evlog_df.to_csv("simulated_evlogs/"+str(run)+"_Eventlog_"+process_entropy+"_"+process_type+".csv",
                        index=False)

    return evlog_df
