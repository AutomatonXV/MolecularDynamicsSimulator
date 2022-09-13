'''
MOLECULAR DYNAMICS SIMULATOR 
        ARNAB SINHA
'''
#################################################
'''
            IMPORTS
'''
import numpy as np
import random as rng
from Particle import ParticleClass
from Simulator import SimulatorClass
#################################################
'''
            PARAMETER DEFINITION
'''
#   Particle Constants
d = 0.1                             # diameter
m = 0.1                             # mass
V_spheres = 4/3*np.pi*(d/2)**3      # volume

#   Simulation Constants
N = 400                             # number of particles
eta = np.pi/15                      # packing fraction
V = d**3 * (N*np.pi/(6*eta))        # volume of primary cube
L = 1
MainSim = SimulatorClass(N, eta)
#################################################
'''
            INITIALIZATION
'''
Sides = int(N**(1/2))
for yPos in range(1,Sides+1):
    for xPos in range(1,Sides+1):
        theta_rng = 2*np.pi*rng.random()
        p = ParticleClass(xPos, yPos, d, m, 1, theta_rng)
        MainSim.Ensemble.append(p)


#################################################
MainSim.Screenshot()