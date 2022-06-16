# -*- coding: utf-8 -*-
"""
The Unity class is responsible for all organizational rules that dictate 
boid behaviour for autopoietic organization. This class has functions to 
promote aggregate behaviour and parameters that can be tuned to change 
experimental conditions. 

Created on Thu Mar 24 11:59:49 2022

@author: Lawrence
"""
import numpy as np
from boid import Boid
from random import randint, random

X, Y = 0,1

class Unity():
    SPACE = 25                # The parameter used to determine allowable space amongst Boids.
    ACCELERATION_RATIO = 1/8  # The delimiter constant for Boid acceleration.
    PURSUE = False            # A flag variabel used to activate active assimilation.
    
    def __init__(self, goal, boids=[], radius=5, generation=0): 
        '''
        The constructor for the Unity class. 

        Parameters
        ----------
        goal : Goal
            The external component the Unity so actively pursue for assimilation.
        boids : List of Boids, optional
            This initial list of Boids or boundary components the Unity should start with. The default is [].
        radius : Integer, optional
            The intial radius value of the unity. The default is 5.
        generation : Integer, optional
            To keep track of what generation the current Unity is from for analyses. The default is 0.

        Returns
        -------
        None.

        '''
        self.boids       = boids 
        self.goal        = goal
        self.radius      = radius
        self.generation  = generation
        self.splits      = 0  # The number of times the unity performs self-reproduction.
        self.metabolised = 0  # The number of external components the Unity metabolizes.
    
    def size(self):
        '''
        This method will return the number of Boids the unity currently has.

        Returns
        -------
        Integer
            Current number of boundary components (Boids).

        '''
        return len(self.boids)
    
    def split(self):
        '''
        This method performs the self-reproduction process by splitting
        the unity in half. Half of the Boids are maintained in the current 
        Unity, while the other half is returned to become a seperate Unity. 

        Returns
        -------
        boids : List of Boids
            The Boids to be used in the second Unity from self-reproduction.

        '''
        mid = self.size()//2
        np.random.shuffle(self.boids)
        boids = self.boids[mid+1:self.size()-1]
        self.boids = self.boids[0:mid]
        self.radius = self.radius/2
        self.splits = self.splits + 1
        for i, boid in enumerate(boids): 
            boid.velocity = boid.velocity/(i+1)
        return boids

    def pursue(self, current_boid):
        '''
        This method is responsible for the change in Boid velocity that will
        result in the Boids minimizing the distance between their current 
        position and the external component they are trying to consume.

        Parameters
        ----------
        current_boid : Boid
            The current Boid being updated.

        Returns
        -------
        Numpy Array
            An array of shape (2,) containing the change in velocity for X and Y.

        '''
        goal = np.array([self.goal.circleX, self.goal.circleY])
        return (goal - current_boid.center)  / 40
    
    def cohesion(self, current_boid):
        '''
        This method is responsible for the change in Boid velocity that will
        result in the Boids being pulled to the barycenter of the Unity to maintain
        structural integrity.

        Parameters
        ----------
        current_boid : Boid
            The current Boid being updated.

        Returns
        -------
        Numpy Array
            An array of shape (2,) containing the change in velocity for X and Y.

        '''
        if self.size() == 1:
            return np.array([0,0])
        
        for boid in self.boids:
            if boid != current_boid:
                current_boid.center = current_boid.center + boid.get_position()
        
        current_boid.center =  current_boid.center / self.size() 
    
        vector = (current_boid.center - current_boid.get_position()) / 100
        return vector
    
    def separation(self, current_boid, flocks):
        '''
        This method is responsible for the change in Boid velocity that will
        result in the Boids steering away fromm one another if they space threshold
        is breeched. 

        Parameters
        ----------
        current_boid : Boid
            The current Boid being updated.

        Returns
        -------
        Numpy Array
            An array of shape (2,) containing the change in velocity for X and Y.

        '''
        vector = np.array([0,0])
        for flock in flocks:
            for boid in flock.boids:
                if boid != current_boid:
                    position1 = current_boid.get_position()
                    position2 = boid.get_position()
                    if np.linalg.norm(position2 - position1) < Unity.SPACE:
                        vector = vector - (position2 - position1)
        return vector
    
    def check_obstacles(self,x,y,current_boid):
        '''
        This method is responsible for collision detection and collision physics.
        When a Boid collides with an object its velocity is reduced and the trajectory
        is altered away from the object. 

        Parameters
        ----------
        x : Float
            The X coordinate the Boid is trying to move to.
        y : Float
            The Y coordinate the Boid is trying to move to.
        current_boid : Boid
            The current Boid being updated.

        Returns
        -------
        Float
            The x coordinate the Boid will move to.
        TYPE
            The y coordinate the Boid will move to.

        '''
        x_range  = range(self.goal.circleX - (self.goal.radius*2), self.goal.circleX + (self.goal.radius*2))
        y_range  = range(self.goal.circleY - self.goal.radius, self.goal.circleY + self.goal.radius)
        pos = np.array([x,y])
        if x in x_range and y in y_range:
            pos = np.array([x,y]) - (np.array([self.goal.circleX,self.goal.circleY]) - current_boid.get_position())
            current_boid.velocity = -current_boid.velocity * 0.1

        return pos[X], pos[Y]

    def check_goal(self, current_boid, goals):
        '''
        This method check the if a current external component is being metabolized.
        It will decay the external component if it is, and assign a new component for
        consumption if its been metabolized.

        Parameters
        ----------
        current_boid : Boid
            The current Boid being updated.
        goals : List of Goals
            All external components in the environment.

        Returns
        -------
        None.

        '''
        if self.goal not in goals:
            self.goal = goals[randint(0, len(goals)-1)]
        radius = self.size()
        center = np.array([int(current_boid.center[X]), int(current_boid.center[Y])])
        x_range_center = list(range(center[X] - radius, center[X] + radius))
        y_range_center = list(range(center[Y] - radius, center[Y] + radius))
        
        x_range_goal  = list(range(self.goal.circleX - self.goal.radius, self.goal.circleX + self.goal.radius))
        y_range_goal  = list(range(self.goal.circleY - self.goal.radius, self.goal.circleY + self.goal.radius))
        
        if any(x in x_range_goal for x in x_range_center) and any(y in y_range_goal for y in y_range_center):
            self.goal.hit()
            if self.goal.health <= 250:
                for _ in range(3):
                    self.boids.append(Boid(self.goal.circleX, self.goal.circleY))
                    self.radius = self.size()/2
                try:
                    goals.remove(self.goal)
                except:
                    print("Goal has been taken already")
                self.goal = goals[randint(0, len(goals)-1)]
                self.metabolised = self.metabolised + 1
        
    
    def update(self, unities=[]):
        '''
        This method is used to update the velocity of all the Boids in the Unity. 
        The organization rules are used to calculate the change in velocity, and
        the velocity is updated accordingly. 

        Parameters
        ----------
        unities : List of Unity, optional
            List of all other Unities to allow for cross-unity collision perception. The default is [].

        Returns
        -------
        None.

        '''
        for i, boid in enumerate(self.boids):
            boid.health = boid.health - random()
            if boid.health <= 0:
                self.boids.pop(i)
                self.radius = self.size()/2
            v1 = self.cohesion(boid)
            v2 = self.separation(boid, unities)
            v3 = self.pursue(boid)
            boid.acceleration = v1 + v2 + (Unity.PURSUE * v3)
            boid.velocity = boid.velocity + boid.acceleration
            boid.limit_velocity()
    
    def check_boundaries(self, x, y, width, height, current_boid):
        '''
        This method is responsible for keeping all unity components within the
        pygame GUI. 

        Parameters
        ----------
        x : Float
            The x coordinate the current boid is attempting to move to.
        y : Float
            The y coordinate the current boid is attempting to move to.
        width : Integer
            The width of the application window for the GUI.
        height : Integer
            The height of the application window for the GUI..
        current_boid : Boid
            The current Boid being updated.

        Returns
        -------
        x : Float
            The x coordinate the Boid will move to.
        y : Float
            The y coordinate the Boid will move to.

        '''
        if x < 0: 
            x = 0
            current_boid.velocity[X] = -current_boid.velocity[X]
        if x > width - Boid.BOID_EXT_WIDTH:
            x = width - Boid.BOID_EXT_WIDTH
            current_boid.velocity[X] = -current_boid.velocity[X]
        if y < 0:
            y = 0
            current_boid.velocity[y] = -current_boid.velocity[Y]
        if y > height - Boid.BOID_EXT_HEIGHT:
            y = height - Boid.BOID_EXT_HEIGHT  
            current_boid.velocity[Y] = -current_boid.velocity[Y]
        return x,y
    
    def move(self, width, height, goals):
        '''
        This method is responsible for the movement of the Boid components using
        the current Boid velocity. It utilizes other methods to validate movement. 

        Parameters
        ----------
        width : Integer
            The width of the application window for the GUI.
        height : TYPE
            The height of the application window for the GUI.
        goals : List of Goals
            All external components in the environment.

        Returns
        -------
        None.

        '''
        for boid in self.boids:
            x   = boid.rect.x + boid.velocity[X]
            y   = boid.rect.y + boid.velocity[Y]
            x,y = self.check_obstacles(x, y, boid)
            x,y = self.check_boundaries(x, y, width, height, boid)
            self.check_goal(boid, goals)
            boid.rect.x = x
            boid.rect.y = y
