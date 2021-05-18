# -*- coding: utf-8 -*-

""" 
File name: satellite.py
Author: Matthew Carroll
Date created: 18/05/2021
Date last modified: 18/05/2021
Python Version: 3.9.5
File Description: Main methods for calculating the satellites state at any time
"""

from celestial_body import Earth, Moon
from global_params import z, G, t, dt, keyframe
from mass import Mass
import math

class Satellite(Mass):
    def satellite_settings(self, 
                        has_deorbited, 
                        procedure_turn_time, 
                        procedure_turn_angle, 
                        turn_off, 
                        target_altitude, 
                        target_altitude_2, 
                        target_moon_alititude, 
                        v_x_0, 
                        v_y_0, 
                        theta, 
                        epsilon, 
                        f_r):
        """
            satellite_settings - Sets and creates initial parameters for use throughout the simulation
        """
        
        self.has_deorbited = has_deorbited # Has the satellite deorbited?
        self.procedure_turn_time = procedure_turn_time # Length of time given for the pitching procedure from the earth surface
        self.procedure_turn_angle = procedure_turn_angle * (math.pi / 180) # Max pitch angle
        self.turn_off = turn_off # Length of total engine burn
        self.target_altitude = target_altitude # Apoapsis
        self.target_altitude_2 = target_altitude_2 # Periapsis
        self.target_moon_altitude = target_moon_alititude # Target altitude in the moons sphere of influence
        
        # Initalise state vectors with correct lengths
        self.alt_earth = [None] * z # Distance between satellite and surface of the earth
        self.m_x = [None] * z       # x component of the satellites position vector wrt the moon
        self.m_y = [None] * z       # y component of the satellites position vector wrt the moon
        self.m_r = [None] * z       # Magnitude of the satellites position vector wrt the moon
        self.alt_moon = [None] * z  # Distance between satellite and surface of the moon
        self.v_x = [None] * z       # x component of the satellites velocity vector
        self.v_y = [None] * z       # y component of the satellites velocity vector
        self.v = [None] * z         # Magnitude of the satellites velocity vector
        self.theta = [None] * z     # Angle of the radius between the two celestial bodies
        self.epsilon = [None] * z   # Angle of the satellites velocity vector
        self.tau = [None] * z       # Angle of the satellites thrust vector
        self.phi = [None] * z       # Angle of the satellites position vector wrt the moon
        self.fg_earth = [None] * z  # Magnitude of the gravitational force exerted by the earth
        self.fg_moon = [None] * z   # Magnitude of the gravitational force exerted by the moon
        self.f_r = [None] * z        # Magnitude of the thrust vector
        self.a_x = [None] * z       # x component of the satellites acceleration vector
        self.a_y = [None] * z       # y component of the satellites acceleration vector
        self.a = [None] * z         # Magnitude of the satellites acceleration vector
        
        # Initial state conditions
        self.alt_earth[0] = 0                                       # Init to sea level on earth
        self.m_x[0] = self.x[0] - Moon.x[0]                         # Init Satellites x position vector wrt moon
        self.m_y[0] = self.y[0] - Moon.y[0]                         # Init Satellites y position vector wrt moon
        self.m_r[0] = math.sqrt(self.m_x[0]**2 + self.m_y[0]**2)    # Magnitude of Satellites position vector wrt moon
        self.alt_moon[0] = self.m_r[0] - Moon.radius                # Altitude above moons surface
        self.v_x[0] = v_x_0                                         # Initial x velocity
        self.v_y[0] = v_y_0                                         # Initial y velocity
        self.v[0] = math.sqrt(self.v_x[0]**2 + self.v_y[0]**2)      # Calculate inital velocity magnitude
        self.theta[0] = theta                                       # Angle of satellites position vector
        self.epsilon[0] = epsilon                                   # Angle of satellites velocity vector
        self.tau[0] = self.epsilon[0]                               # Angle of satellites thrust vector
        
        # Depending on the direction in which satellite is travelling, 
        # set the angle of satellites position vector relative to the moon
        if self.y[0] >= Moon.y[0]:
            self.phi[0] = math.acos(self.m_x[0] / self.m_r[0])
        elif self.y[0] < Moon.y[0]:
            self.phi[0] = (math.pi * 2) - math.acos(self.m_x[0] / self.m_r[0])
        else:
            print("ERROR: Could not calculate the satellites position vector wrt the moon!")
        
        self.fg_earth[0] = -G * Earth.mass * self.mass / self.r[0] ** 2 # Inital value of earths gravity force acting on satellite
        self.fg_moon[0] = -G * Moon.mass * self.mass / self.m_r[0] ** 2 # Inital value of moons gravity force acting on satellite
        self.f_r[0] = f_r                                               # Set initial thrust to the value given by the user
        self.a_x[0] = (self.fg_earth[0] * math.cos(self.theta[0]) + \
                       self.f_r[0] * math.cos(self.epsilon[0])) / self.mass # Initalise x acceleration of satellite
        self.a_y[0] = (self.fg_earth[0] * math.sin(self.theta[0]) + \
                       self.f_r[0] * math.sin(self.epsilon[0])) / self.mass # Initalise y acceleration of satellite
        self.a[0] = math.sqrt(self.a_x[0]**2 + self.a_y[0]**2) ## Initalise acceleration magnitude of satellite
        
        # Used to determine how many method calls were required to carry out a maneuver
        self.accel_procedure_turn_called = 0
        self.thrust_earth_in_circle_called = 0
        self.thrust_earth_in_ellipse_called = 0
        self.thrust_moon_in_circle_called = 0
        
        # Time of satelite deorbiting
        self.deorbit_time = 0
        
    def calc_position(self, 
                      i,
                      temp_moon_x_list,
                      temp_moon_y_list,
                      temp_satellite_x_list,
                      temp_satellite_y_list):
        """
            calc_position - Use eulers method to calculate the position at next time step
        """
        # Calculate x, y position of satellite
        self.x[i+1] = self.x[i] + self.v_x[i] * dt + 0.5 * self.a_x[i] * dt**2
        self.y[i+1] = self.y[i] + self.v_y[i] * dt + 0.5 * self.a_y[i] * dt**2
        
        # Calculate the new position vector
        self.r[i+1] = math.sqrt(self.x[i+1]**2 + self.y[i+1]**2)
        
        # Determine altitude above the earths surface
        self.alt_earth[i+1] = self.r[i+1] - Earth.radius
        
        # Calculate the x, y position of the satellite relative to the moon
        self.m_x[i+1] = self.x[i+1] - Moon.x[i+1]
        self.m_y[i+1] = self.y[i+1] - Moon.y[i+1]
        
        # Determine the position vector of the satellite relative to the moon
        self.m_r[i+1] = math.sqrt(self.m_x[i+1]**2 + self.m_y[i+1]**2)
        
        # Get altitude above the moons surface
        self.alt_moon[i+1] = self.m_r[i+1] - Moon.radius
        
        # Loop through adding values to the lists that will be dumped into a csv file
        while i in keyframe:
            temp_moon_x = Moon.x[i+1] / Earth.radius
            temp_moon_y = Moon.y[i+1] / Earth.radius
            temp_satellite_x = Photon.x[i+1] / Earth.radius
            temp_satellite_y = Photon.y[i+1] / Earth.radius
            temp_moon_x_list.append(temp_moon_x)
            temp_moon_y_list.append(temp_moon_y)
            temp_satellite_x_list.append(temp_satellite_x)
            temp_satellite_y_list.append(temp_satellite_y)
            break
    
    def calc_velocity(self, i):
        """
            calc_velocity - Use eulers method to calculate the velocity at next time step
        """
        
        # Calculate the x, and y velocity 
        self.v_x[i+1] = self.v_x[i] + self.a_x[i] * dt
        self.v_y[i+1] = self.v_y[i] + self.a_y[i] * dt
        
        # Calculate the velocity magnitude
        self.v[i+1] = math.sqrt(self.v_x[i+1]**2 + self.v_y[i+1]**2)
        
    def calc_force(self, i):
        """
            calc_force - Determine the gravitational force on the earth, and the thrust produced by the satellite
        """
        self.fg_earth[i+1] = -G * Earth.mass * self.mass / self.r[i+1] ** 2 # Grav force formula for the earth
        self.fg_moon[i+1] = -G * Moon.mass * self.mass / self.m_r[i+1] ** 2 # Grav force formula for the moon
        
        # Check if the satellite is still able to burn
        if t[i+1] < Photon.turn_off:
            self.f_r[i+1] = self.f_r[0]
        else:
            self.f_r[i+1] = 0
    
    def calc_angles(self, i):
        """
            calc_angles - Determines the angle of the vectors such as position, velocity, thrust and position relative to the moon
        """
        
        # Swap vector direction depending on the y component of the velocity
        
        if self.v_y[i+1] >= 0:
            self.epsilon[i+1] = math.acos(self.v_x[i+1] / self.v[i+1])
        elif self.v_y[i+1] < 0:
            self.epsilon[i+1] = (2 * math.pi) - math.acos(self.v_x[i+1] / self.v[i+1])
        else:
            print("ERROR: Could not calculate the angle of the satellites velocity vector! At time: ", t[i+1])

        if self.y[i+1] >= 0:
            self.theta[i+1] = math.acos(self.x[i+1] / self.r[i+1])
        elif self.y[i+1] < 0:
            self.theta[i+1] = (2 * math.pi) - math.acos(self.x[i+1] / self.r[i+1])
        else:
            print("ERROR: Could not calculate theta angle for the r vector!")
            
        if self.y[i+1] >= Moon.y[i+1]:
            self.phi[i+1] = math.acos(self.m_x[i+1] / self.m_r[i+1])
        elif self.y[i+1] < Moon.y[i+1]:
            self.phi[i+1] = (2 * math.pi) - math.acos(self.m_x[i+1] / self.m_r[i+1])
        else:
            print("ERROR: Could not calculate phi angle for the satellites position vector wrt the moon! At time: ", t[i+1])

    def calc_normal_acceleration(self, i):
        """
            calc_normal_acceleration - Calculates the normal acceleration of the satelite based on the thrust direction
        """
        
        # Calc thrust angle
        self.tau[i+1] = self.epsilon[i+1]
        
        # Calc acceleration x and y
        self.a_x[i+1] = (self.fg_earth[i+1] * math.cos(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.cos(self.phi[i+1]) + \
                         self.f_r[i+1] * math.cos(self.tau[i+1])) / self.mass
        self.a_y[i+1] = (self.fg_earth[i+1] * math.sin(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.sin(self.phi[i+1]) + \
                         self.f_r[i+1] * math.sin(self.tau[i+1])) / self.mass
        
        # Calc acceleration vector
        self.a[i+1] = math.sqrt(self.a_x[i+1]**2 + self.a_y[i+1]**2)
    
    def calc_accel_procedure_turn(self, i):
        """
            calc_accel_procedure_turn - Determines the acceleration during the pitching procedure after take-off
        """
        
        # Add 1 to the number of times this method has run
        self.accel_procedure_turn_called += 1
        
        # Calculate acceleration rotated by the turn-over angle
        a_tx = self.v[i+1] * math.cos(self.procedure_turn_angle) - self.v_x[i+1]
        a_ty = self.v[i+1] * math.sin(self.procedure_turn_angle) - self.v_y[i+1]
        
        # Acceleration during turn over
        a_t = math.sqrt(a_tx**2 + a_ty**2)
        
        # Switch thrust angle direction depending on the direction the acceleration is occuring 
        if a_ty >= 0:
            self.tau[i+1] = math.acos(a_tx / a_t)
        elif a_ty < 0:
            self.tau[i+1] = (2 * math.pi) - math.acos(a_tx / a_t)
        else:
            print("ERROR: Could not calculate tau angle for the satellites thrust vector in the acceleration procedure turn! At time: ", t[i+1])

        # Calculate the satelite acceleration
        self.a_x[i+1] = (self.fg_earth[i+1] * math.cos(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.cos(self.phi[i+1]) + \
                         self.f_r[i+1] * math.cos(self.tau[i+1])) / self.mass
        self.a_y[i+1] = (self.fg_earth[i+1] * math.sin(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.sin(self.phi[i+1]) + \
                         self.f_r[i+1] * math.sin(self.tau[i+1])) / self.mass
        self.a[i+1] = math.sqrt(self.a_x[i+1]**2 + self.a_y[i+1]**2)
        
    def calc_thrust_earth_circular(self, i):
        """
            calc_thrust_earth_circular - Calculate the amount of delta-v needed for a circular orbit of the user-inputted altitude
        """
        
        # Add 1 to the number of times this method has been called
        self.thrust_earth_in_circle_called += 1
        gamma = (math.pi / 2) + self.theta[i+1] # Angle of the velocity orbit vector
        v_o = math.sqrt(Earth.mu * self.r[i+1]) / self.r[i+1] # velocity orbit vector
        
        # Turnover acceleration
        a_tx = (v_o * math.cos(gamma) - self.v_x[i+1]) / dt
        a_ty = (v_o * math.sin(gamma) - self.v_y[i+1]) / dt
        a_t = math.sqrt(a_tx**2 + a_ty**2)
        
        # Thrust angle direction swaps depending on the direction of the acceleration
        if a_ty >= 0:
            self.tau[i+1] = math.acos(a_tx / a_t)
        elif a_ty < 0:
            self.tau[i+1] = (2 * math.pi) - math.acos(a_tx / a_t)
        else:
            print("ERROR: Could not calculate tau angle for the satellites thrust vector in circular orbit around Earth! At time: ", t[i+1])
        
        # Calculate the new thrust and accelerations based on previous values
        self.f_r[i+1] = self.mass * a_t
        self.a_x[i+1] = (self.fg_earth[i+1] * math.cos(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.cos(self.phi[i+1]) + \
                         self.f_r[i+1] * math.cos(self.tau[i+1])) / self.mass
        self.a_y[i+1] = (self.fg_earth[i+1] * math.sin(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.sin(self.phi[i+1]) + \
                         self.f_r[i+1] * math.sin(self.tau[i+1])) / self.mass
        self.a[i+1] = math.sqrt(self.a_x[i+1]**2 + self.a_y[i+1]**2)
        print("IN A CIRCULAR ORBIT AROUND EARTH AT T+", t[i+1], "s INTO THE FLIGHT")
        
    def calc_thrust_earth_elliptical(self, i, r_a):
        """
            calc_thrust_earth_elliptical - Calculate the amount of delta-v needed for an elliptical orbit of the user-inputted altitude
        """
        
        # Add 1 to the number of times this method has been called
        self.thrust_earth_in_ellipse_called += 1
        
        # Direction of the orbit velocity vector
        gamma = (math.pi / 2) + self.theta[i+1] # Angle of the velocity orbit vector
        
        # Calculate the orbit velocity
        v_o = math.sqrt(2 * Earth.mu * \
                        (r_a + Earth.radius) * (self.r[i+1]) / \
                        ((r_a + Earth.radius) + (self.r[i+1]))) / \
                        self.r[i+1]
                        
        # Calculate turn over acceleration
        a_tx = (v_o * math.cos(gamma) - self.v_x[i+1]) / dt
        a_ty = (v_o * math.sin(gamma) - self.v_y[i+1]) / dt
        a_t = math.sqrt(a_tx**2 + a_ty**2)
        
        # Thrust angle direction swaps depending on the direction of the acceleration 
        if a_ty >= 0:
            self.tau[i+1] = math.acos(a_tx / a_t)
        elif a_ty < 0:
            self.tau[i+1] = (2 * math.pi) - math.acos(a_tx / a_t)
        else:
            print("ERROR: Could not calculate tau angle for the satellites thrust vector in elliptical orbit around Earth! At time: ", t[i+1])

        # Calculate the new thrust and acceleration values
        self.f_r[i+1] = self.mass * a_t
        self.a_x[i+1] = (self.fg_earth[i+1] * math.cos(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.cos(self.phi[i+1]) + \
                         self.f_r[i+1] * math.cos(self.tau[i+1])) / self.mass
        self.a_y[i+1] = (self.fg_earth[i+1] * math.sin(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.sin(self.phi[i+1]) + \
                         self.f_r[i+1] * math.sin(self.tau[i+1])) / self.mass
        self.a[i+1] = math.sqrt(self.a_x[i+1]**2 + self.a_y[i+1]**2)
        print("IN AN ELLIPTICAL ORBIT AROUND EARTH AT T+", t[i+1], "s INTO THE FLIGHT")
        
    def calc_thrust_moon_circular(self, i):
        """
            calc_thrust_moon_circular - Calculate the amount of delta-v needed for a circular orbit around the moon of the user-inputted altitude
        """
        
        # Add 1 to the number of times this method has been called
        self.thrust_moon_in_circle_called += 1
        
        gamma = self.phi[i+1] - (math.pi / 2)     # Angle of spacecrafts velocity vector around the earth
        lambda_moon = Moon.omega[i+1] + (math.pi / 2) # Angle of spacecrafts velocity vector around the moon
        
        # Velocity vector of the moon
        v_m = math.sqrt(Earth.mass * G / Moon.dE)
        
        # Velocity vector of the earth
        v_o = math.sqrt(Moon.mu * self.m_r[i+1]) / self.m_r[i+1]
        
        # Turn over acceleration
        a_tx = (v_o * math.cos(gamma) + v_m * \
                math.cos(lambda_moon) - self.v_x[i+1]) / dt
        a_ty = (v_o * math.sin(gamma) + v_m * \
                math.sin(lambda_moon) - self.v_y[i+1]) / dt
        a_t = math.sqrt(a_tx**2 + a_ty**2)
        
        # Thrust angle direction swaps depending on the direction of the acceleration 
        if a_ty >= 0:
            self.tau[i+1] = math.acos(a_tx / a_t)
        elif a_ty < 0:
            self.tau[i+1] = (2 * math.pi) - math.acos(a_tx / a_t)
        else:
            print("ERROR: Could not calculate tau angle for the satellites thrust vector in circular orbit around Moon! At time: ", t[i+1])

        # Calculate the new thrust force and acceleration values
        self.f_r[i+1] = self.mass * a_t
        self.a_x[i+1] = (self.fg_earth[i+1] * math.cos(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.cos(self.phi[i+1]) + \
                         self.f_r[i+1] * math.cos(self.tau[i+1])) / self.mass
        self.a_y[i+1] = (self.fg_earth[i+1] * math.sin(self.theta[i+1]) + \
                         self.fg_moon[i+1] * math.sin(self.phi[i+1]) + \
                         self.f_r[i+1] * math.sin(self.tau[i+1])) / self.mass
        self.a[i+1] = math.sqrt(self.a_x[i+1]**2 + self.a_y[i+1]**2)
    
    def calc_acceleration(self, i):
        """
            calc_acceleration - Conditionals to determine which part of acceleration phase of the flight the satellite is in
        """
        # if t[i+1] > self.procedure_turn_time and \
        #    self.procedure_turn_angle - self.epsilon[i] > 0 and \
        #    self.thrust_earth_in_circle_called == 0:
        #        self.calc_accel_procedure_turn(i)
        if t[i+1] > self.procedure_turn_time and \
            self.target_altitude + 500000 > self.alt_earth[i+1] > \
            self.target_altitude and \
            self.thrust_earth_in_circle_called == 0 and \
            self.thrust_earth_in_ellipse_called == 0:
                self.calc_thrust_earth_circular(i)
        elif t[i+1] > self.procedure_turn_time and \
            self.target_altitude + 500000 > self.alt_earth[i+1] > \
            self.target_altitude - 500000 and \
            self.x[i+1] >= 0 and self.y[i+1] < 0 and \
            self.thrust_earth_in_ellipse_called == 0 and \
            self.thrust_earth_in_circle_called == 1:
                self.calc_thrust_earth_elliptical(i, self.target_altitude_2)
        elif t[i+1] > self.procedure_turn_time and \
             self.target_altitude_2 + 5e5 > self.alt_earth[i+1] > \
             self.target_altitude_2 and \
             self.thrust_earth_in_circle_called == 1 and \
             self.thrust_earth_in_ellipse_called == 1:
                 self.calc_thrust_earth_circular(i)
        elif t[i+1] > self.procedure_turn_time and \
             self.target_altitude_2 + 5e5 > self.alt_earth[i+1] > \
             self.target_altitude_2 - 5e5 and \
             self.x[i+1] >= 0 and self.y[i+1] < 0 and \
             self.thrust_earth_in_circle_called == 2 and \
             self.thrust_earth_in_ellipse_called == 1:
                 self.calc_thrust_earth_elliptical(i, (Moon.dE - Earth.radius))
        elif t[i+1] > self.procedure_turn_time and \
             225 * (math.pi / 180) > self.epsilon[i] > 180 * (math.pi / 180) and \
             Moon.dE + 5e5 > self.alt_earth[i+1] > Moon.dE and \
             self.thrust_earth_in_circle_called == 2 and \
             self.thrust_moon_in_circle_called == 0:
                 self.calc_thrust_earth_circular(i)
        elif t[i+1] > self.procedure_turn_time and \
             self.target_moon_altitude > self.alt_moon[i+1]:
                 self.calc_thrust_moon_circular(i)
        else:
            self.calc_normal_acceleration(i)
            
    def calc_deorbit(self, i):
        """
            calc_deorbit - Will determine when the satellite has deorbited
        """
        if self.alt_earth[i+1] <= 0.0 or self.alt_moon[i+1] <= 0.0:
            print("Deorbited at ", t[i+1], "s")
            self.has_deorbited = True
            self.deorbit_time = t[i+1]
        else:
            pass

# Create a satellite object
Photon = Satellite(100, Earth.radius + 1e6, 0.0)
Photon.satellite_settings(False, 0, 0, 30, 1e6, 10e6, 1e6, \
                         0.0, 0.0, 0.0, 0.001*(math.pi / 180), 1200)