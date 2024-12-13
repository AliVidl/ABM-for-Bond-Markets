# """
# This code includes work derived from https://github.com/tpike3/SugarScape?tab=MIT-1-ov-file
# Copyright (c) 2018 Tom Pike
# Licensed under the MIT License
# Significant alterations have occurred and is copyright 2023 Alicia Vidler




from mesa import Agent
import math
from scipy.stats.mstats import gmean
from numpy import round
from collections import defaultdict

from global_data import append_to_df

import csv
import os

class NetAgent(Agent):
    
    '''
    
    Agent initiation creates:
        -identify type
        -agent position on grid
        -Neighborhood type
        -Accumulation: accounts for how much agents has
        -Capability: accounts for what agent can do 
    '''
    
    def __init__(self, unique_id, pos, model, metabolism = {},\
                 accumulations = {}, capability = {}, Moore = False):
        super().__init__(unique_id, model)
        self.type = "agent"
        self.pos = pos
        self.moore = Moore
        #Data set up = {sug_bolism : Sugar Value, spice_bolism : Spice Value}
        self.metabolism = metabolism
        #Data set up = {1 : Sugar Value, 2 : Spice Value}
        self.accumulations = accumulations
        self.capability = capability
        #MRS = Marginal Rate of Substitution
        self.MRS = self.calc_MRS()
        self.welfare = self.calc_welfare()
        self.status = "alive"
        self.price = defaultdict(list)
        

        
        
    def __str__(self):
        return "Agent"
    
    ##########################################################################
    #
    #         Helper Functions
    #
    #########################################################################   
    
    
    def calc_MRS(self):
        """
        Calculates agent's Marginal Rate of Substitution (MRS)
        preference of wanting more sugar or spice
        
        Formulation  GrAs p. 102
        """
                        
        MRS =  (self.accumulations[2.0]/self.metabolism["spice_bolism"])/ \
                   (self.accumulations[1.0]/self.metabolism["sug_bolism"])
        return MRS
    
    def calc_welfare(self):
        
        '''
        Calculates Agents Welfare based on sugar and spice
        accumulation and metabolism
        
        Formulation GrAS p. 97
        '''
        
        
        
        meta = self.metabolism["sug_bolism"] + self.metabolism["spice_bolism"]
        sug_welfare = self.accumulations[1.0]**(self.metabolism["sug_bolism"]/meta)
        spice_welfare = self.accumulations[2.0]**(self.metabolism["spice_bolism"]/meta)
        
       
        if isinstance(sug_welfare, complex):
            sug_welfare = 0
           
            
        if isinstance(spice_welfare, complex): 
            spice_welfare = 0
               
            
        return (sug_welfare, spice_welfare)
    
    def get_distance(self, pos_1, pos_2):
        """ 
        Get the distance between two points
        
        Args:
            pos_1, pos_2: Coordinate tuples for both points.
        """
        x1, y1 = pos_1
        x2, y2 = pos_2
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx ** 2 + dy ** 2)
    
    def no_agent(self, pos):
        
        '''
        Helper Function for self.move(): 
            
        Checks if anything in cell, all cells have resource
        so if list more than 1 item must contain agent
        '''
        this_cell = self.model.grid.get_cell_list_contents([pos])
        
        return len(this_cell) <= 1
    
    def find_trader (self):
        '''
        Helper Function for self.trade(): 
            
        gets_agents from nearby to trade with
        '''
        
        
        traders = []
        neighbors = [i for i in self.model.grid.get_neighborhood(self.pos, \
                   self.moore, radius = self.capability['vision'])]
                
        for n in neighbors: 
            this_cell = self.model.grid.get_cell_list_contents([n])
            for item in this_cell: 
                if str(item) == "Agent":
                    traders.append(item) 
        return traders
    
    def draft_trade(self, sugar, spice, partner):
        
        meta = self.metabolism["sug_bolism"] + self.metabolism["spice_bolism"]
        p_meta = partner.metabolism["sug_bolism"] + partner.metabolism["spice_bolism"]
        
        if (self.accumulations[2.0] - spice) <= 0 or \
           (partner.accumulations[1.0] - sugar <= 0): 
               return False
                
        spice_gain_wel = \
        (partner.accumulations[2.0]+spice)**(partner.metabolism["spice_bolism"]/p_meta)
        spice_loss_wel = \
        (self.accumulations[2.0]-spice)**(self.metabolism["spice_bolism"]/meta)
        sug_gain_wel = \
        (self.accumulations[1.0]+sugar)**(self.metabolism["sug_bolism"]/meta)
        sug_loss_wel = \
        (partner.accumulations[1.0]-sugar)**(partner.metabolism["sug_bolism"]/p_meta)
       
        
        
        MRS_self_draft = ((self.accumulations[2.0]-spice)/self.metabolism["spice_bolism"])/ \
               ((self.accumulations[1.0]+sugar)/self.metabolism["sug_bolism"])
        
        MRS_partner_draft = ((partner.accumulations[2.0]+spice)/partner.metabolism["spice_bolism"])/ \
               ((partner.accumulations[1.0]-sugar)/partner.metabolism["sug_bolism"])
        
        if (spice_gain_wel * sug_loss_wel) >= (partner.welfare[0] * partner.welfare[1]) and \
            (sug_gain_wel * spice_loss_wel) >= (self.welfare[0] * self.welfare[1]) and (MRS_self_draft >=\
            MRS_partner_draft): 
                return True
        else:
                return False
        
             
        
    def poss_welfare(self,sugar, spice):
        
        meta = self.metabolism["sug_bolism"] + self.metabolism["spice_bolism"]
        sug_welfare = sugar**(self.metabolism["sug_bolism"]/meta)
        spice_welfare = spice**(self.metabolism["spice_bolism"]/meta)
        
       
        if isinstance(sug_welfare, complex):
            sug_welfare = 0
           
            
        if isinstance(spice_welfare, complex): 
            spice_welfare = 0
               
            
        return (sug_welfare, spice_welfare)
    
    
    def assess_sustenance(self, pos): 
        '''
        Helper Function to self.move()
        
        Identifies what sites will give most welfare
        
        GrAS p. 98; Appendix C
        '''       
        
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if agent.type == "resource":
                poss_sug = self.accumulations[1.0] + agent.value_sug
                poss_spice = self.accumulations[2.0] +agent.value_spice
                
                welfare_poss = self.poss_welfare(poss_sug, poss_spice)
                return (welfare_poss[0] * welfare_poss[1])
        return 0
    ##########################################################################
    #
    #          Principle Step Functions
    #
    #########################################################################   
    
    
    def assess_welfare(self):
        '''
        Assess need for sugar and spice
        Welfare function  GrAS p. 97
        Determine Marignal Rate of Substitution (MRS) 
        GrAS p. 102
        '''
                      
        self.welfare =self.calc_welfare()
    
        self.MRS = self.calc_MRS()
    
     
    def move(self):
        '''
        Movement function 
        
        GrAS p. 98-99
        
        '''
        self.assess_welfare()        
        # Get neighborhood within vision
        neighbors = [i for i in self.model.grid.get_neighborhood(self.pos, \
                    self.moore, radius=self.capability["vision"]) \
                    if self.no_agent(i)]
        
        #Provides possibility of not moving
        neighbors.append(self.pos)
    
        max_welfare = max([self.assess_sustenance(pos) for pos in neighbors])
        
        candidates = [pos for pos in neighbors if \
                      self.assess_sustenance(pos) == max_welfare]
        if len(candidates) == 0: 
            self.random.shuffle(neighbors)
            final_candidates =  neighbors
        else: 
            
            min_dist = min([self.get_distance(self.pos, pos) for pos in candidates])
            final_candidates = [pos for pos in candidates if self.get_distance(self.pos,
                pos) == min_dist]
            self.random.shuffle(final_candidates)
 
        if final_candidates[0] == self.pos: 
            pass
        else: 
            self.model.grid.move_agent(self, final_candidates[0])
            
    def trade(self):
        '''
        Trade Function 
        
        GrAS p. 105
        '''
        
        self.assess_welfare()
        
        traders = self.find_trader()
     
        price = 0
        self.model.price_record[self.model.step_num][self.unique_id]= (0,0)
       


        if len(traders) > 0: 
            self.random.shuffle(traders) 
        else: 
            return
        
        
        for partner in traders: 
       
            if self.MRS == partner.MRS: 
                continue
           
        
            else: 
                #Calculate Price
                price = gmean([self.MRS, partner.MRS])
               
                #Draft Trade
                if price > 0:     
                    spice = price
                    sugar = 0.001   
                else:
                    continue
                 
                    
                    
                    
                
                if self.MRS > partner.MRS: 
                    conduct = self.draft_trade(sugar, spice, partner)
                    if conduct == True: 
                        self.accumulations[1] += sugar
                        self.accumulations[2] -= spice
                        partner.accumulations[2] += spice
                        partner.accumulations[1] -= sugar
                        
                        self.assess_welfare()
                        partner.assess_welfare()
                    else: 
                        continue

                        
                        
                else: 
                    conduct = partner.draft_trade(sugar, spice, self)
                    if conduct == True:
                        self.accumulations[1] -= sugar
                        self.accumulations[2] += spice
                        partner.accumulations[2] -= spice
                        partner.accumulations[1] += sugar
                        self.assess_welfare()
                        partner.assess_welfare()
                       
                    else: 
                        continue

        self.model.price_record[self.model.step_num][self.unique_id]= (price, partner.unique_id)

        
    
    def eat(self):


        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        for res in this_cell:
            if res.type == "resource":
                self.accumulations[1] += (res.value_sug - self.metabolism["sug_bolism"])
                self.accumulations[2] += (res.value_spice - self.metabolism["spice_bolism"])
                res.value_sug = 0
                res.value_spice = 0
    
    def die(self): 
        if self.accumulations[1] <= 0.1 or self.accumulations[2] <= 0.1: 

            self.status = "dead"
           
            self.model.ml.remove(self)
            self.model.grid.remove_agent(self)
            
    
    
                
    ########################################################################
    #    #
    #             STEP FUNCTION
    #
    ######################################################################    
    
    
    def step(self):
       
        # Core Movement Functions
        self.move()
        self.eat()
        self.die()

        
        if self.status == "dead":
            self.pos = (99, 99)
            self.save_data(dead=True)  
            return
        self.trade()
        self.save_data(dead=False)
    
    
    

    def save_data(self, dead):
        row = {
            "Run": self.model.run,
            "Step Number": self.model.step_num,
            "Status": self.status,
            "Unique ID": self.unique_id,
            "Capability": self.capability['vision'],
           
            "Metabolism Sug Bolism": self.metabolism['sug_bolism'],
            "Metabolism Spice Bolism": self.metabolism['spice_bolism'],
            "Accumulations Sugar": self.accumulations[1],
            "Accumulations Spice": self.accumulations[2],
            "Welfare Sug": self.welfare[0],
            "Welfare SPICE": self.welfare[1],
            "Pos": str(self.pos),
            "MRS": str(self.MRS),
            "Price": self.model.price_record[self.model.step_num][self.unique_id][0] if not dead else None,
            "TradePartnerUID": self.model.price_record[self.model.step_num][self.unique_id][1] if not dead else None
        }
        append_to_df(row)
