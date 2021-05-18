# -*- coding: utf-8 -*-

""" 
File name: mass.py
Author: Matthew Carroll
Date created: 18/05/2021
Date last modified: 18/05/2021
Python Version: 3.9.5
File Description: Creates and handles the mass of objects i.e. planet, moon, satellite
"""

from global_params import G, z
import math

class Mass:
    def __init__(self, m, x_0, y_0):
        self.mass = m
        self.mu = G * m     # Gravitational constants used in physics calcs
        self.x = [None] * z # Init x position vector
        self.y = [None] * z # Init y position vector
        self.r = [None] * z # Init radius vector
        self.x[0] = x_0     # Inital condition for x
        self.y[0] = y_0     # Initial condition for y
        self.r[0] = math.sqrt(x_0**2 + y_0**2) # Inital condition for radius
        