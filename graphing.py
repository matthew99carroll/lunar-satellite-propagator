# -*- coding: utf-8 -*-

""" 
File name: graphing.py
Author: Matthew Carroll
Date created: 18/05/2021
Date last modified: 18/05/2021
Python Version: 3.9.5
File Description: Creates and handles all of the graphing of the data
"""

from global_params import t
from celestial_body import Moon, Earth
from satellite import Photon
import matplotlib.pyplot as plt
import math

# Set font size and dark mode
plt.rcParams.update({'font.size': 8})
plt.style.use('dark_background')

def graph_common_settings(i):
    """
        graph_common_settings - Some common graph properties that are often used
    """
    plt.xlim(xmin=0)
    plt.xlim(xmax=t[i+1])
    plt.hlines(0, t[0], t[i+1], "gray", linewidth=0.5)
    plt.grid(color='white', linestyle='-', linewidth=1)
    
def graph_position(i):
    """
        graph_position - Graphs the X, Y position of the Photon satelite along with the altitude above the earth and moon
    """
    plt.figure(num=1, figsize=(8,8), dpi=100)
    plt.subplot(221)
    plt.title('t, Photon X position')
    plt.plot(t, Photon.x, "orange")
    graph_common_settings(i)
    plt.subplot(222)
    plt.title('t, Photon Y position')
    plt.plot(t, Photon.y, "orange")
    graph_common_settings(i)
    plt.subplot(223)
    plt.title('t, Photon Altitude Above Earth')
    plt.plot(t, Photon.alt_earth, "orange")
    plt.hlines(Photon.target_altitude, t[0], t[i+1], "gray", linewidth=0.5)
    plt.hlines(Photon.target_altitude_2, t[0], t[i+1], "gray", linewidth=0.5)
    graph_common_settings(i)
    plt.subplot(224)
    plt.title('t, Photon Altitude Above Moon')
    plt.plot(t, Photon.alt_moon, "orange")
    plt.hlines(Photon.target_moon_altitude, t[0], t[i+1], "gray", linewidth=0.5)
    graph_common_settings(i)
    plt.tight_layout(w_pad=2.0, h_pad=2.0)

def graph_velocity(i):
    """
        graph_velocity - Graphs the X, Y velocity of the Photon satelite along with the magnitude of the velocity vector
    """
    plt.figure(num=2, figsize=(8,8), dpi=100)
    plt.subplot(221)
    plt.title('t, Photon velocity x')
    plt.plot(t, Photon.v_x, "green")
    graph_common_settings(i)
    plt.subplot(222)
    plt.title('t, Photon velocity y')
    plt.plot(t, Photon.v_y, "green")
    graph_common_settings(i)
    plt.subplot(223)
    plt.title('t, Photon velocity magnitude')
    plt.plot(t, Photon.v, "green")
    graph_common_settings(i)
    plt.tight_layout(w_pad=2.0, h_pad=2.0)
    
def graph_acceleration(i):
    """
        graph_acceleration - Graphs the X, Y acceleration of the Photon satelite along with the magnitude of the acceleration vector
    """
    plt.figure(num=3, figsize=(8,8), dpi=100)
    plt.subplot(221)
    plt.title('t, Photon acceleration x')
    plt.plot(t, Photon.a_x, "red")
    graph_common_settings(i)
    plt.subplot(222)
    plt.title('t, Photon acceleration y')
    plt.plot(t, Photon.a_y, "red")
    graph_common_settings(i)
    plt.subplot(223)
    plt.title('t, Photon acceleration magnitude')
    plt.plot(t, Photon.a, "red")
    graph_common_settings(i)
    plt.tight_layout(w_pad=2.0, h_pad=2.0)
    
def graph_force(i):
    """
        graph_force - Graphs the gravity force of the earth and moon acting on Photon along with the thrust force being produced by photo
    """
    plt.figure(num=4, figsize=(8,8), dpi=100)
    plt.subplot(221)
    plt.title('t, Photon Force Gravity Earth')
    plt.plot(t, Photon.fg_earth, "purple")
    graph_common_settings(i)
    plt.subplot(222)
    plt.title('t, Photon Force Gravity Moon')
    plt.plot(t, Photon.fg_moon, "purple")
    graph_common_settings(i)
    plt.subplot(223)
    plt.title('t, Photon Thrust Force')
    plt.plot(t, Photon.f_r, "purple")
    graph_common_settings(i)
    plt.tight_layout(w_pad=2.0, h_pad=2.0)
    
def graph_angle_settings(i):
    """
        graph_angle_settings - Some common graph properties that are often used when plotting angles
    """
    plt.hlines(0, t[0], t[i+1], "gray", linewidth=0.5)
    plt.hlines((math.pi / 2), t[0], t[i+1], "gray", linewidth=0.5)
    plt.hlines(math.pi, t[0], t[i+1], "gray", linewidth=0.5)
    plt.hlines((math.pi * 3 / 2), t[0], t[i+1], "gray", linewidth=0.5)
    plt.hlines((math.pi * 2), t[0], t[i+1], "gray", linewidth=0.5)
    plt.xlim(xmin=0)
    plt.xlim(xmax=t[i+1])
    plt.ylim(ymin=0)
    plt.ylim(ymax=(2 * math.pi))
    
def graph_angles(i):
    """
        graph_angles - Graphs the following parameters with time:
                        Epsilon - The angle of satellites velocity vector
                        Theta   - The angle of satellites position vector
                        Phi     - The angle of satellites position vector with respect to the moon
                        Tau     - The angle of satellites thrust vector
    """    
    plt.figure(num=5, figsize=(8,8), dpi=100)
    plt.subplot(221)
    plt.title('t, Photon Epsilon')
    plt.plot(t, Photon.epsilon, color="blue")
    graph_angle_settings(i)
    plt.subplot(222)
    plt.title('t, Photon Theta')
    plt.plot(t, Photon.theta, color="blue")
    graph_angle_settings(i)
    plt.subplot(223)
    plt.title('t, Photon Phi')
    plt.plot(t, Photon.phi, color="blue")
    graph_angle_settings(i)
    plt.subplot(224)
    plt.title('t, Photon Tau')
    plt.plot(t, Photon.tau, color="blue")
    graph_angle_settings(i)
    plt.tight_layout(w_pad=2.0, h_pad=2.0)

def graph_earth_proximity():
    """
        graph_earth_proximity - Plots the satelites altitude changes and Hohmann transfers to reach higher orbits
    """    
    fig = plt.figure(num=6, figsize=(8,8), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    plt.title("Earth Orbit Visualisation")
    plt.plot(Photon.x, Photon.y, color="orange")
    plt.xlim(xmin=-Earth.radius - 3e7)
    plt.xlim(xmax=Earth.radius + 3e7)
    plt.ylim(ymin=-Earth.radius - 3e7)
    plt.ylim(ymax=Earth.radius + 3e7)
    ax.add_patch(plt.Circle((0,0), Earth.radius, color="green", fill=None))
    ax.add_patch(plt.Circle((0,0), Photon.target_altitude + Earth.radius, 
                            color="blue", fill=None))
    ax.add_patch(plt.Circle((0,0), Photon.target_altitude_2 + Earth.radius, 
                            color="blue", fill=None))
    ax.add_patch(plt.Circle((Photon.x[t.index(max(t))],
                                       Photon.y[t.index(max(t))]), 
                            5e4, color="orange", fill=True))
    plt.grid(color='white', linestyle='-', linewidth=1)
    
def graph_moon_proximity(i):
    """
        graph_earth_proximity - Plots the satelites orbit changes around the moon
    """    
    fig = plt.figure(num=7, figsize=(8,8), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    plt.title("Lunar Orbit Visualisation")
    plt.plot(Photon.x, Photon.y, color="orange")
    plt.xlim(xmin=Moon.x[i+1] - 5.0e6)
    plt.xlim(xmax=Moon.x[i+1] + 5.0e6)
    plt.ylim(ymin=Moon.y[i+1] - 5.0e6)
    plt.ylim(ymax=Moon.y[i+1] + 5.0e6)

    ax.add_patch(plt.Circle((0,0), Earth.radius, color="green", fill=None))
    ax.add_patch(plt.Circle((Photon.x[t.index(max(t))],
                                       Photon.y[t.index(max(t))]),
                            5e4, color="orange", fill=True))
    ax.add_patch(plt.Circle((Moon.x[t.index(max(t))],Moon.y[t.index(max(t))]), 
                            5e4, color="#377EB8", fill=True))
    ax.add_patch(plt.Circle((Moon.x[t.index(max(t))],Moon.y[t.index(max(t))]), 
                            Moon.radius, color="#377EB8", fill=None))
    ax.add_patch(plt.Circle((Moon.x[t.index(max(t))],Moon.y[t.index(max(t))]), 
                            Moon.radius + Photon.target_moon_altitude, 
                            color="purple", fill=None))    
    plt.grid(color='white', linestyle='-', linewidth=1)
    
def graph_earth_surface():
    """
        graph_earth_surface - Plot focusing on the ascent from the earths surface. Not of particular interest
                              considering that the interest is on the Photon satelite stage of the flight
    """    
    fig=plt.figure(num=8, figsize=(8,8), dpi=100)
    ax=fig.add_subplot(1,1,1)
    plt.title('Earth Surface')
    plt.plot(Photon.x, Photon.y, color="orange")
    plt.xlim(xmin=Earth.radius-1e4)
    plt.xlim(xmax=Earth.radius+1e6*2)
    plt.ylim(ymin=-1e6)
    plt.ylim(ymax=1e6)
    plt.hlines(0, -Moon.dE, Moon.dE, "white", linewidth=1.0)
    plt.vlines(0, -Moon.dE, Moon.dE, "white", linewidth=1.0)
    ax.add_patch(plt.Circle((0,0), Earth.radius, color="green", fill=None))
    ax.add_patch(plt.Circle((Photon.x[t.index(max(t))],
                                       Photon.y[t.index(max(t))]), 
                            5e3, color="orange", fill=True))
    plt.grid(color='white', linestyle='-', linewidth=1)
 
def graph_earth_moon_exact():
    """
        graph_earth_moon_exact - Plot that shows the Hohmann transfer to reach the orbit of the moon
    """
    fig=plt.figure(num=9, figsize=(8,8), dpi=100)
    ax=fig.add_subplot(1,1,1)
    plt.title('Earth Moon')
    plt.plot(Moon.x, Moon.y, color="#377EB8")
    plt.plot(Photon.x, Photon.y, color="orange")
    plt.xlim(xmin=-Moon.dE)
    plt.xlim(xmax=Moon.dE)
    plt.ylim(ymin=-Moon.dE + 1e6)
    plt.ylim(ymax=Moon.dE + 1e6)
    plt.hlines(0, -Moon.dE, Moon.dE, "white", linewidth=1.0)
    plt.vlines(0, -Moon.dE, Moon.dE, "white", linewidth=1.0)
    ax.add_patch(plt.Circle((0,0), Earth.radius, color="green", fill=None))
    ax.add_patch(plt.Circle((Moon.x[t.index(max(t))],Moon.y[t.index(max(t))]), 
                            Moon.radius, color="#377EB8", fill=None))
    ax.add_patch(plt.Circle((Photon.y[t.index(max(t))],
                                       Photon.y[t.index(max(t))]), 
                            5e4, color="orange", fill=True))
    plt.grid(color='white', linestyle='-', linewidth=1)
    
def graph_earth_moon_margin():
    """
        graph_earth_moon_margin - Plot that shows the Hohmann transfer to reach the orbit of the moon, 
                                  but additionally adds the orbit of the moon around the earth for context
    """
    fig=plt.figure(num=10, figsize=(8,8), dpi=100)
    ax=fig.add_subplot(1,1,1)
    plt.title('Earth Moon')
    plt.plot(Moon.x, Moon.y, color="#377EB8")
    plt.plot(Photon.x, Photon.y, color="orange")
    plt.xlim(xmin=-Moon.dE - 1e8)
    plt.xlim(xmax=Moon.dE + 1e8)
    plt.ylim(ymin=-Moon.dE - 1e8)
    plt.ylim(ymax=Moon.dE + 1e8)
    plt.hlines(0, -Moon.dE - 1e8, Moon.dE + 1e8, "white", linewidth=1.0)
    plt.vlines(0, -Moon.dE - 1e8, Moon.dE + 1e8, "white", linewidth=1.0)
    ax.add_patch(plt.Circle((0,0), Moon.dE, color="gray", fill=None))
    ax.add_patch(plt.Circle((0,0), Earth.radius, color="green", fill=None))
    ax.add_patch(plt.Circle((Moon.x[t.index(max(t))],Moon.y[t.index(max(t))]), 
                            Moon.radius, color="#377EB8", fill=None))
    ax.add_patch(plt.Circle((Photon.y[t.index(max(t))],
                                       Photon.y[t.index(max(t))]), 
                            5e4, color="orange", fill=True))
    plt.grid(color='white', linestyle='-', linewidth=1)

def graph_deorbit_site(i):
    """
        graph_deorbit_site - Will plot the deorbit site of the Photon satelite if the parameters set for the vehicle are not correct.
                           i.e. Not enough thrust, shallow turn angle, short burn times
    """
    fig=plt.figure(num=11, figsize=(8,8), dpi=100)
    ax=fig.add_subplot(1,1,1)
    plt.title('Deorbit Site')
    plt.plot(Photon.x, Photon.y, color="orange")
    plt.plot(Photon.x[i], Photon.y[i], color="orange")
    plt.xlim(xmin=-Earth.radius - 3e7)
    plt.xlim(xmax=Earth.radius + 3e7)
    plt.ylim(ymin=-Earth.radius - 3e7)
    plt.ylim(ymax=Earth.radius + 3e7)
    ax.add_patch(plt.Circle((0,0), Earth.radius, color="green", fill=None))
    ax.add_patch(plt.Circle((Photon.x[Photon.deorbit_time],Photon.y[Photon.deorbit_time]), 1e3, color="orange", fill=True))
    ax.add_patch(plt.Circle((Moon.x[Photon.deorbit_time],Moon.y[Photon.deorbit_time]), Moon.radius, color="#377EB8", fill=None))
    plt.grid(color='white', linestyle='-', linewidth=1)
      
def show_plots():
    """
        show_plots - Simply shows the plots
    """
    plt.show()