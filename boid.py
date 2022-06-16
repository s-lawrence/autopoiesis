# -*- coding: utf-8 -*-
"""
This class is the Boid class used to represent the individual
boundary compontents. In this class there are helper functions
and parameters used by the system.

Created on Mon Mar  7 14:18:26 2022

@author: Lawrence
"""
import os
import pygame 
import numpy as np
import math
from random import random, randint

X, Y = 0, 1

class Boid():
    
    BOID_EXT_IMAGE = pygame.image.load(
        os.path.join("Assets", "exterior_boid.png"))  # The image path for the Boid design
    BOID_EXT_WIDTH, BOID_EXT_HEIGHT = 11, 30          # The pixel width and height of the Boid
    MAX_VEL = 2                                       # Maximum velocity for the Boids
    MIN_VEL = np.array([0.5, 0.5])                    # Minimum velocity for the Boids
    
    def __init__(self, x=300, y=300):
        '''
        The constructor function for the Boid class. 

        Parameters
        ----------
        x : Integer, optional
            This dictactes the initial x coordinate of the Boid. The default is 300.
        y : Integer, optional
            s dictactes the initial y coordinate of the Boid. The default is 300.

        Returns
        -------
        None.

        '''
        self.velocity     = Boid.MIN_VEL              # The current velocity of the Boid
        self.acceleration = np.array([0,0])           # The current accelelration of the Boid
        self.angularV     = 0.07                      # The Angular velocity of the Boid
        self.center       = np.array([x,y])           # The percieved barycenter of the unity.
        self.radians      = random()                  # Current rotation of the Boid.
        self.surface      = pygame.transform.rotate(  # The pygame surface to display the Boid.
                            pygame.transform.scale(
                                Boid.BOID_EXT_IMAGE, 
                                (Boid.BOID_EXT_WIDTH, 
                                 Boid.BOID_EXT_HEIGHT)),180)
        self.rect         = pygame.Rect(x, y,         # The pygame rect class to position the Boid.
                                        Boid.BOID_EXT_WIDTH, Boid.BOID_EXT_HEIGHT)
        self.health       = randint(1000, 3000)       # The current health of the Boid.

    def get_position(self):
        '''
        This method returns the current position of the Boid from the 
        pygame rect class.

        Returns
        -------
        Numoy Array
            Return the current x, y position of the Boid as a numpy array.

        '''
        return np.array([self.rect.x,self.rect.y])
     
    def limit_velocity(self):
        '''
        THis method is responsible for delimiting the Boids velocity
        to be within the maximum allowed velocity. 

        Returns
        -------
        None.

        '''
        if abs(self.velocity[X]) > Boid.MAX_VEL:
            self.velocity[X] = (self.velocity[X] / abs(self.velocity[X])) * Boid.MAX_VEL
        if abs(self.velocity[Y]) > Boid.MAX_VEL:
            self.velocity[Y] = (self.velocity[Y] / abs(self.velocity[Y])) * Boid.MAX_VEL   

    def rotate(self):
        '''
        This method is responsible for manipulating the pygame classes, Rect and Surface, to 
        display the Boid with the proper orientation given its currect trajectory
        around the barycenter. 

        Returns
        -------
        rotated_image : pygame.Surface
            A new pygame suface that has been orientated to match the Boid's trajeectory.
        rotated_image_rect : pygame.Rect
            A new pygame Rect that now contains the oriented x, and y coordinates.

        '''
        originPos = [7.5,20]
        self.angle   = (self.radians * (180/math.pi) * -1) + 90
        image_rect = self.surface.get_rect(topleft = (self.rect.x - originPos[X], self.rect.y-originPos[Y]))
        offset_center_to_pivot = pygame.math.Vector2([self.rect.x, self.rect.y]) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-self.angle)
        rotated_image_center = (self.rect.x - rotated_offset.x, self.rect.y - rotated_offset.y)
        rotated_image = pygame.transform.rotate(self.surface, self.angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        return rotated_image, rotated_image_rect