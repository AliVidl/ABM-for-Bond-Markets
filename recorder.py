# """
# This code includes work derived from https://github.com/tpike3/SugarScape?tab=MIT-1-ov-file
# Copyright (c) 2018 Tom Pike
# Licensed under the MIT License
# Significant alterations have occurred and is copyright 2023 Alicia Vidler



# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 06:09:24 2018

@author: ymamo
"""



import NetAgent as N

def survivors(model):
    
    alive =  model.ml.agents_by_type[N.NetAgent]
    
   
    return len(alive)

def get_agent_health(model):
    
    for k,v in model.ml.agents_by_type[N.NetAgent].items():
        model.datacollector.add_table_row("Health", {"Agent":v.unique_id, \
                                          "Sugar_Level": v.accumulations[1], \
                                          "Spice_Level": v.accumulations[2], 
                                          "Step": model.step_num})
    
def get_time(model,time):
    model.datacollector.add_table_row("Time", {"Time Per Step": time})
    
def get_price(model):
    price_record = {}
    for k,v in model.ml.agents_by_type[N.NetAgent].items():
        price_record[k] = v.price
        
    return price_record
