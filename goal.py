# -*- coding: utf-8 -*-
"""
This class is the class to represent the external components used when the unity
performs active assimilation.

Created on Fri Mar 25 09:40:06 2022

@author: Lawrence
"""
from random import randint

class Goal():
    def __init__(self):
        self.circleX = randint(100,1500) # X coordinate of the external component
        self.circleY = randint(100,800)  # Y coordinate of the external component
        self.radius  = 10                # Radius of the external component
        self.health  = 1000              # Initial health of the external component
        
    def hit(self):
        '''
        This method is responsible for reducing the health of the external component
        (performing motabolic decaying).

        Returns
        -------
        None.

        '''
        self.health -= 1
        
    def color(self):
        '''
        This method returns the curent color of the external component which
        changes throughout the metabolic process. As the health of the external
        component decreases the color begins to fade and becomes darker. 

        Returns
        -------
        r : Float
            RGD value for the red.
        g : Float
            RGD value for the green.
        b : Float
            RGD value for the blue.

        '''
        r, g, b = max(0,0.1*self.health), max(0,0.2*self.health), max(0,0.1*self.health)
        return (r, g, b)