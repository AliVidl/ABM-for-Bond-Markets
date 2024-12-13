"""
This code includes work derived from https://github.com/tpike3/SugarScape?tab=MIT-1-ov-file
Copyright (c) 2018 Tom Pike
Licensed under the MIT License
Significant alterations have occurred and is copyright 2023 Alicia Vidler


# -*- coding: utf-8 -*-
"""
Created on Dec 02 2021

@author: Alicia Vidler
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 05:50:24 2018

@author: Tom Pike

Sugarscape Model as base for test for ANT and MAP
Original Rob axtell and Joshua Epstein "Growing Artificial Societies: 
    Social Science from the Bottom Up"
    Washington D.C: Brookings Institute Press 1996

Adapted from Mesa 0.8.4 Jackie Kazil and David Masad
"""

from collections import defaultdict
import time
import itertools

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


import multilevel_mesa as mlm
import apto_processes as ap
import Landscape
import ResourceScape as R
import NetAgent as N
import recorder
import numpy as np




class NetScape(Model):
    
    def __init__(self, run, height = 50, width = 50, initial_population =200, \
                 Moore = False, torus = True, regrow = 1, seed = None):
        
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
        #Mesa Agent Scheduler
        #self.schedule = schedule.RandomActivationByBreed(self)
        self.ml = mlm.MultiLevel_Mesa(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.regrow = regrow
        self.running = True
        self.price_record = defaultdict(defaultdict)  #av         self.zero_resource = None
                      
        
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
        #places resources from landscape on grid
        for k,v in landscape.items(): 
            resource =  R.resource(k, self, v, self.regrow)
            self.grid.place_agent(resource, (resource.pos[0], resource.pos[1]))
            #POINT
            self.ml.add(resource)
            
        
               
        #fills in empty grids with null value resource agent        
        #Deviation from GrAS -- in empty cells has random resource from 0 to 4
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
        vision_array = np.random.randint(1,50,self.initial_population)
        # AV this is where vision is set all previous Feb 2023 1 to 6 
#AV come here to fix vision and inital accumulation
        spice_array = np.random.randint(1,5,self.initial_population)
        sugar_array = np.random.randint(1,5,self.initial_population)

        # AV this is where metabolism has been set  1 to 6 


        for n in range(self.initial_population):
            #x = 0
            #y = 0
            #print ("position: ", (n, x,y))
            #GrAS p. 108
            sugar = self.random.randrange(49,50)
            spice = self.random.randrange(49,50)

            # AV this is where initall accumulation of resources occurs... 
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
            self.ml.add(a ) # AV , schedule = False)
            self.grid.place_agent(a,pos_array[n])

        
     
    ######################################################################
    #
    #
    #       Step function
    #
    ########################################################################    
        
        
    def step(self):
        time_step0 = time.time()
        
        print ("STEP ", self.step_num)
        self.ml.form_group(ap.form_connection, self)        
        self.ml.step() 
        time_step1 = time.time() - time_step0
        self.datacollector.collect(self)
        recorder.get_agent_health(self)
        recorder.get_time(self,time_step1)
        self.ml.reassess_group(ap.reassess)
        #print ("\n")
        self.step_num += 1
            
            

