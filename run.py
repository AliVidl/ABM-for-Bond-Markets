 -*- coding: utf-8 -*-
"""
Created on Dec 02 2021

@author: ymamo
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 07:02:35 2018

@author: ymamo
"""

from NetScape import NetScape
import NetAgent
import pickle
import recorder

survivors = []
time = []
price_df = {}

for run in range(100):
    print ("Run: ", run)
    test = NetScape(run, height = 50, width = 50, initial_population = 4, regrow = 0, seed = 42)
    
    for s in range(4000):
        test.step()

    df = test.datacollector.get_table_dataframe("Time") 
    price_df["Run"+str(run)] = test.price_record
    agents = recorder.survivors(test)
    survivors.append(agents)
    time.append(df["Time Per Step"].sum())
