import numpy as np

PHOTON_PARAMETERS = {
                     "EARTH_ALTITUDE": 1e6, 
                     "MOON_ALTITUDE": 1e6, 
                     "THRUST": 1200, 
                     "MASS": 100
                     }


z = int(600000) # - Time in seconds to run simulation

G = 6.67e-11 # Gravitational constant

# Simulaton time step parameters
t = [None] * z
t[0] = 0
dt = 1

# Dump to file parameters
keyframe = np.arange(0, z, 500)
