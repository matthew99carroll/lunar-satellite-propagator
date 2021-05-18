# -*- coding: utf-8 -*-

""" 
File name: propagate.py
Author: Matthew Carroll
Date created: 18/05/2021
Date last modified: 18/05/2021
Python Version: 3.9.5
File Description: Runs the main simulation, plots the data and dumps the data to a csv file.
"""

from global_params import z, t, dt
from celestial_body import Earth, Moon
from satellite import Photon
import math
import graphing

# Initialise lists
temp_moon_x_list = []
temp_moon_y_list = []
temp_Photon_x_list = []
temp_Photon_y_list = []

# Append initial conditions
temp_moon_x_list.append(Moon.x[0] / Earth.radius)
temp_moon_y_list.append(Moon.y[0] / Earth.radius)
temp_Photon_x_list.append(Photon.x[0] / Earth.radius)
temp_Photon_y_list.append(Photon.y[0] / Earth.radius)

def run_simulation():
    """
        run_simulation - Loops through all time, and calculates the position of the celestial bodies, and the Photon satelite
        After finishing the main simulation loop it will export the data to a csv file, and use matplotlib to plot the results
    """

    print("Running propagator please wait...")

    for i in range(z - 1):
        
        t[i+1] = t[i] + dt
        
        Moon.calc_position(i)
        Moon.calc_moon_angle(i)
        
        Photon.calc_position(i,
                            temp_moon_x_list,
                            temp_moon_y_list,
                            temp_Photon_x_list,
                            temp_Photon_y_list)
        
        Photon.calc_velocity(i)
        Photon.calc_force(i)
        Photon.calc_angles(i)
        Photon.calc_acceleration(i)
        Photon.calc_deorbit(i)
        
        if Photon.has_deorbited:
            break
        else:
            pass
        
    dump_to_file("./data.csv")  
    plot_results(i)

def plot_results(i):
    """
        plot_results - Will take the state vectors and plot them, if the vehicle fails to escape earths gravity it will deorbit and crash
    """
    
    if Photon.has_deorbited:
        # Only show deorbit plot
        graphing.graph_deorbit_site(i)
    else:
        # Show all graphs
        graphing.graph_position(i)
        graphing.graph_velocity(i)
        graphing.graph_acceleration(i)
        graphing.graph_force(i)
        graphing.graph_angles(i)
        graphing.graph_earth_proximity()
        graphing.graph_moon_proximity(i)
        graphing.graph_earth_moon_margin()
        
        # UNCOMMENT IF YOU WISH TO SEE THESE PLOTS
        #graphing.graph_earth_moon_exact()
        #graphing.graph_earth_surface() 
    
    graphing.show_plots()
    
def dump_to_file(filename):
    """
        dump_to_file - Simple dump of vehicle x, y position and the moons x, y position. Can be easily expanded on it more data is of interest
    """
    # Dumb lists of satellite position and moon position
    open(filename, "w").write("temp_moon_x_list = " + str(temp_moon_x_list) + '\n' \
                                + "temp_moon_y_list = " + str(temp_moon_y_list) + "\n" \
                                + "temp_Photon_x_list = " + str(temp_Photon_x_list) + "\n" \
                                + "temp_Photon_y_list = " + str(temp_Photon_y_list) + '\n')
    
# Run the simulation
run_simulation()