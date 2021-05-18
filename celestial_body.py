# -*- coding: utf-8 -*-

""" 
File name: celestial_body.py
Author: Matthew Carroll
Date created: 18/05/2021
Date last modified: 18/05/2021
Python Version: 3.9.5
File Description: Creates and handles all of the parameters required for a celestial body includng
                  calculations of its position
"""

from mass import Mass
from global_params import z, t
import math

class CelestialBody(Mass):
    
    def body_settings(self, radius, period, dE):
        """
            body_settings - General settings for the celestial body such as
                            size, orbital period, distance between parent body,
                            sphere of influence
        """
        self.radius = radius     # Radius of body
        self.period = period * 24 * 60 * 60 # Total days to rotate once around its parent body
        self.dE = dE             # Distance between bodies
        self.soi = (self.mass / Earth.mass) ** 0.4 * self.radius # Sphere of influence
        
    def calc_position(self, i):
        """
            calc_position - Determines the position of the body in orbit around its parent body at any time
        """
        self.x[i+1] = self.dE * math.cos(2  * math.pi / self.period * t[i+1] + self.omega[0])
        self.y[i+1] = self.dE * math.sin(2 * math.pi / self.period * t[i+1] + self.omega[0])
        self.r[i+1] = math.sqrt(self.x[i+1]**2 + self.y[i+1]**2)
        
    def init_moon_angle(self):
        """ 
        init_moon_angle - Calculates the inital angle of the moon conditionally based on the y position.
                          The initial angle relies on the inital x and r position of the moon
        """
        self.omega = [None] * z
        
        if self.y[0] >= 0:
            # Inital angle of moon
            self.omega[0] = math.acos(self.x[0] / self.r[0])
        elif self.y[0] < 0:
            # Inital angle of moon
            self.omega[0] = (2 * math.pi) - math.acos(self.x[0] / self.r[0])
        else:
            print("ERROR: Could not calculate initial angle of the moon based on the values given!")
    
    def calc_moon_angle(self, i):
        """ Calculates the new angle of the moon conditionally based on the most current y position """
        if self.y[i+1] >= 0:
            self.omega[i+1] = math.acos(self.x[i+1] / self.r[i+1])
        elif self.y[i+1] < 0:
            self.omega[i+1] = (2 * math.pi) - math.acos(self.x[i+1] / self.r[i+1])
        else:
            print("ERROR: Could not calculate new angle of the moon based on the current values!")

# Earth's celestial body
Earth = CelestialBody(5.97237e+24, 0.0, 0.0)
Earth.body_settings(6.3781e+6, 365, 0.0)

# Moon's celestial body
Moon = CelestialBody(7.342e+22, 364658999.01580966, 121599365.28529961)
Moon.body_settings(1.7371e+6, 30, 3.84399e+8)
Moon.init_moon_angle()