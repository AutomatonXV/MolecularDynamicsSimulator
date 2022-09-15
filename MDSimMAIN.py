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
import time 
#################################################
'''
            PARAMETER DEFINITION
'''
#   Particle Constants
d = 0.1                             # diameter
m = 0.1                             # mass
V_spheres = 4/3*np.pi*(d/2)**3      # volume

#   Simulation Constants
N = 16                             # number of particles
eta = np.pi/15                      # packing fraction
V = d**3 * (N*np.pi/(6*eta))        # volume of primary cube
L = 1

PairsPossible = 1/2 * N * (N-1)
print("The total number of pairs possible are   ", PairsPossible)

MainSim = SimulatorClass(N, eta)
#################################################
'''
            INITIALIZATION
'''
Sides = int(N**(1/2))
for yPos in range(1,Sides+1):
    for xPos in range(1,Sides+1):
        theta_rng = 2*np.pi*rng.random()
        p = ParticleClass(xPos, yPos, d, m, 1, theta_rng, MainSim)
        MainSim.Ensemble.append(p)

MainSim.ConstructPairs()

SimulationStartTime = time.time()
MainSim.Screenshot()
while MainSim.COLLISIONS < MainSim.MAX_COLLISIONS and MainSim.t0 < MainSim.MAXTIME:
        #reset collision objects
        MainSim.CollisionObject = None
        MainSim.ShortestCollision = None
        #Check for pair collision
        for pairs in  MainSim.Pairs: 
                if not pairs.isApproaching(): continue
                if not pairs.isColliding(): continue
                pairs.updateCollisionTime()
                #print(pairs.Tc)

        #Check for wall collision
        for particles in MainSim.Ensemble:
                particles.updateWallCollision()

        #print(MainSim.CollisionObject)
        #print("Shortest Time",MainSim.ShortestCollision)
        
        MainSim.StepForward()
        MainSim.Screenshot()
        print("COLLISION %\t",100* MainSim.COLLISIONS/MainSim.MAX_COLLISIONS, "%, \tSIM. TIME\t", MainSim.t0)
        #################################################
SimulationEndTime = time.time() 
Elapsed = SimulationEndTime - SimulationStartTime
print("TOTAL TIME ELAPSED:\t", Elapsed)
MainSim.Movie()