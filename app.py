# -*- coding: utf-8 -*-
"""
This class is responsible for the overall control of fthe application. It instantiates the pygame
interface and regulates the frame updates. This class is composed of the following methods: 
    1) self_reproduction()
    2) update_boid_positions()
    3) update_goals()
    4) get_random_goal()
    5) draw_window()
    6) main()
    7) print_results()

Created on Sun Mar  6 11:13:47 2022

@author: Steven Lawrence
"""

import math
import pygame 
import pandas as pd
from boid import Boid
from unity import Unity
from goal import Goal
from random import randint
from datetime import datetime, timedelta


FPS        = 60                                        # Defines the numnber of frames per second to run application at.
X, Y       = 0,1                                       # Globals to denote the 'X' and 'Y' dimensions.
BLACK      = (0,0,0)                                   # RGB color code for Black.
WHITE      = (255,255,255)                             # RGB color code for White.
WIDTH      = 1800                                      # Width of application screen. 
HEIGHT     = 1000                                      # Height of application screen.
WIN        = pygame.display.set_mode((WIDTH, HEIGHT))  # Global variable for application window.
unities    = []                                        # A global list to hold all active unities in the application. 
INIT_GOALS = 5                                         # The number of initial external components to start the application with. 
goals      = [Goal() for _ in range(INIT_GOALS)]       # The global list that hold all external components in the application.


def self_reproduction(unity) -> None:
    '''
    This method performs the self-reproduction steps on a given unity
    and appends the new unity to the global list. 

    Parameters
    ----------
    unity : Unity
        The Unity to be split into two via self-reproduction..

    Returns
    -------
    None

    '''
    boids = unity.split()
    goal  = get_random_goal()
    new_unity = Unity(goal, boids, generation=unity.generation+1)
    unities.append(new_unity)
    
def update_boid_positions() -> None:
    '''
    This method calls the update and move method for each Boid in the unity 
    resulting in the x, y positions to be updated. Additional checks are
    performed to remove dead unities, or to trigger self-reproduction.
    
    Returns
    -------
    None
        Updates Boid components in unties by reference.

    '''
    for unity in unities:
        if unity.size() == 0:
            unities.remove(unity)
        if unity.size() >= 20:
            self_reproduction(unity)
        unity.update(unities)
        unity.move(WIDTH, HEIGHT, goals)

def update_goals() -> None:
    '''
    This method is responsible for regulating the regeneration
    of external components. Once the number of external componeents
    decreases past a threshold, more are generated with some stochasticity. 
    
    Returns
    -------
    None
         Updates the global goals list.

    '''
    if len(goals) <= 3:
        for _ in range(randint(0,2)):
            goals.append(Goal())

def get_random_goal() -> Goal:
    '''
    This method will return a random Goal from the global goals list. 
    This randomness is to reduce the competitive nature of the unities
    over external components after self-reproduction occurs promoting
    the lifecyle of both unities

    Returns
    -------
    Goal
         The next external component the unity should target.
    '''
    return goals[randint(0, len(goals)-1)]
  
def draw_window() -> None:
    '''
    Returns
    -------
    None
            This method is responsible for updating the user interface via the pygame library. 
            For every frame the window must be refilled with the background color, external 
            components need to be updated, and the unity movements need to be displayed. .

    '''
    WIN.fill(BLACK)
    for goal in goals:
        pygame.draw.circle(WIN, goal.color(), (goal.circleX, goal.circleY), goal.radius)
    for unity in unities:
        if unity.size() == 0: continue
        pygame.draw.circle(WIN, WHITE, (unity.boids[0].center[X], unity.boids[0].center[Y]), unity.size())
        for boid in unity.boids:
            boid.radians = (boid.radians + boid.angularV) % (2*math.pi)
            boid.rect.x = (boid.rect.x) + math.cos(boid.radians) * unity.radius
            boid.rect.y = (boid.rect.y) + math.sin(boid.radians) * unity.radius
            rotated_boid, origin = boid.rotate()
            WIN.blit(rotated_boid, origin)
    pygame.display.update()
    
def main() -> None:
    '''
    This method is the main application loop that will run continuously
    until the set time limit has occured or a used quits the application. 
    The loop is responsible for regulating frames per second, managing 
    update method calls, and handling application termination.
    
    Returns
    -------
    None
    
    '''
    clock = pygame.time.Clock()
    run = True
    end_time = datetime.now() + timedelta(minutes = 30)
    counter = 0
    unities.append(Unity(goal=get_random_goal()))
    while datetime.now() < end_time and run:
        clock.tick(FPS)
        if counter % 10 == 0 and counter <= 100:
            unities[0].boids.append(Boid())
            if counter == 100: 
                Unity.PURSUE = True
        counter = counter + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        update_goals()
        update_boid_positions()       
        draw_window()
    print_results()
    pygame.quit()

def print_results() -> None:
    '''
    This method ouputs the data for eaach unity based on generations. A data frame
    is constructed to display the generational statistics which may be used for 
    analyses. 

    Returns
    -------
    None

    '''
    data = {"Generation": [], "Number of Splits": [], "Metabolised": []}
    for unity in unities:
        data["Generation"].append(unity.generation)
        data["Number of Splits"].append(unity.splits)
        data["Metabolised"].append(unity.metabolised)
    df = pd.DataFrame(data=data)
    print(df)

if __name__ == "__main__":
    '''
    Responsible for ensuring only one instance of this class is ever intiated by the main process.
    '''
    main()