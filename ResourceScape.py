# """
# This code includes work derived from https://github.com/tpike3/SugarScape?tab=MIT-1-ov-file
# Copyright (c) 2018 Tom Pike
# Licensed under the MIT License
# Significant alterations have occurred and is copyright 2023 Alicia Vidler



from mesa import Agent


class resource(Agent):
    
    def __init__(self, unique_id, model, attrs, regrow):
        super().__init__(unique_id, model)
        self.pos = unique_id
        self.value_sug = attrs[0]
        self.value_spice = attrs[1]
        self.max_sug = attrs[0]
        self.max_spice = attrs[1]
        self.type = "resource"
        self.regrow = regrow
        
    def __str__(self):
        return "Resource"
        
    
    ######################################################################
    #
    #
    #             STEP FUNCTION
    #
    ######################################################################  

    
    def step(self):
        '''
            Regrow resource 
        '''
        
        self.value_spice = min([self.max_spice, self.value_spice + self.regrow])
        self.value_sug = min([self.max_sug, self.value_sug + self.regrow])
        
            
            
                
        
