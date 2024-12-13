# """
# This code includes work derived from https://github.com/tpike3/SugarScape?tab=MIT-1-ov-file
# Copyright (c) 2018 Tom Pike
# Licensed under the MIT License
# Significant alterations have occurred and is copyright 2023 Alicia Vidler


from collections import defaultdict
import time
import itertools

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


import multilevel_mesa as mlm

import Landscape
import ResourceScape as R
import NetAgent as N
import recorder
import numpy as np




class NetScape(Model):
    
   
    def __init__(self, run, height=50, width=50, initial_population=4, \
                 Moore= False, torus= True, regrow=1, seed=42, \
                 vision_array=None, spice_array=None, sugar_array=None, \
                    sugar_range=(25, 50), spice_range=(25, 50)):

           
        '''
        Args:
            height - y axis of grid_size
            width - x axis of grid size
            initial_population - number of agents starting
            moore - type of neighborhood
            torus - whether or no world wraps
            regrow - amout each resource grows bas each step
            process - Number of additonal proces by agents
            0 = Movement/Survive; 1 = +trade, 2 = +
            
        Initial Parameters: 
            Multigrid
            ActivationbyBreed (see schedule)
            Num_Agents counter to account for each agent number
            timekeeper - dictionary to keep track of time for each section
            start_time - create initial time
            datacollector to collect agent data of model
        '''
      
      

        self.step_num = 0
        self.run = run
        self.height = height
        self.width = width
        self.initial_population = initial_population
        self.num_agents = 0
        
        self.ml = mlm.MultiLevel_Mesa(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.regrow = regrow
        self.running = True
        self.price_record = defaultdict(defaultdict)  
 
        
        '''
        Recorders
          Start datacollector
          Start time recorder
        '''
        self.start_time = time.time()
        
        self.datacollector = DataCollector(\
                             model_reporters = {"MetaAgent": recorder.survivors}, \
                             tables ={"Health":["Agent", "Step", "Sugar_Level", \
                                                "Spice_Level"], \
                             "Time":["Time Per Step"]})
        
        
        '''
        
        Creates the landscape:
            Fours mounds 2 sugar, 2 spice located- 1 in each quadrant
            imports landscape module to account for various landscape sizes
        '''
        self.resource_dict = {}
        
        landscape = Landscape.create_landscape(height, width)

        
        for k,v in landscape.items(): 
            resource =  R.resource(k, self, v, self.regrow)
            adjusted_pos = self.grid.torus_adj((resource.pos[0], resource.pos[1]))  #
            self.grid.place_agent(resource, adjusted_pos)
          
            self.ml.add(resource)
               
        
        for a,x,y in self.grid.coord_iter():
            if a == set():
                resource = R.resource((x,y), self, \
                                      (self.random.randrange(0,2), \
                                       self.random.randrange(0,2)),self.regrow)
                self.grid.place_agent(resource, (resource.pos[0], resource.pos[1]))
                #POINT
                self.ml.add(resource)
                        
           
        '''
        Creates the agents:
            
        '''
        '''  AV reset vision, metabolism HERE '''
    
        pos_array = list(self.ml.agents_by_type[R.resource].keys())
        self.random.shuffle(pos_array)
        
        
        # If arrays are not provided, generate them
        if vision_array is None:
            vision_array = np.random.randint(1, 6, self.initial_population)
        if spice_array is None:
            spice_array = np.random.randint(1, 6, self.initial_population)
        if sugar_array is None:
            sugar_array = np.random.randint(1, 6, self.initial_population)

        # AV edit
        self.sugar_range = sugar_range
        self.spice_range = spice_range




        for n in range(self.initial_population):
          
            
            sugar = self.random.randrange(*self.sugar_range)
            spice = self.random.randrange(*self.spice_range)
            
            # sugar = self.random.randrange(49,50)
            # spice = self.random.randrange(49,50)

       
            
            #GrAS p.108
            sug_bolism = sugar_array[n]
            spice_bolism = spice_array[n]
            #GrAS p. 108
            vision = vision_array[n]
            neighbors = Moore
            a = N.NetAgent(n, pos_array[n], self, \
                                 {"sug_bolism": sug_bolism, \
                                 "spice_bolism": spice_bolism}, \
                                 {1 : sugar, 2: spice}, {"vision": vision}, \
                                 neighbors)
            #POINT
            self.ml.add(a ) 
            self.grid.place_agent(a,pos_array[n])

        
     
    ######################################################################
    #
    #
    #       Step function
    #
    ########################################################################    
        
        
    def step(self):
        time_step0 = time.time() 
        self.ml.step() 
        time_step1 = time.time() - time_step0
        self.datacollector.collect(self)
        recorder.get_agent_health(self)
        recorder.get_time(self,time_step1)

        self.step_num += 1
            
            

