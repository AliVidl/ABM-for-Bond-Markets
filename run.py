
"""
This code includes work derived from https://github.com/tpike3/SugarScape?tab=MIT-1-ov-file
Copyright (c) 2018 Tom Pike
Licensed under the MIT License
Significant alterations have occurred and is copyright 2023 Alicia Vidler

"""

from NetScape import NetScape
import NetAgent
#import visualization
import pickle
import recorder
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from global_data import write_to_csv


for run in range(10):
   
    print ("Run: ", run)
   
    
    sugar_range = (40, 55)      # Agent initial range of resources
    spice_range = (40, 55)      # Agent intial range of resource =2
    initial_population = 4 #20      # number of agents (overrides netscape assumption)
    vision_array = np.random.randint(1, 50, initial_population)  #range for vision assigned to agents
    spice_array = np.random.randint(1, 2, initial_population)   # Metabolism to resouce 1 range, randomly asigned to agents at step -0
    sugar_array = np.random.randint(1, 2, initial_population)   # Metabolism 2 for agents

    test = NetScape(run, height = 50, width = 50,  initial_population=initial_population, regrow = 0, seed = 0, \
                     vision_array = vision_array, spice_array =spice_array, sugar_array=sugar_array, \
                          sugar_range=sugar_range, spice_range=spice_range, torus= True)
   
   
  
    for s in range(150):
        test.step()

    # write to DF and csv in Global_data.py
        
    write_to_csv()


############


