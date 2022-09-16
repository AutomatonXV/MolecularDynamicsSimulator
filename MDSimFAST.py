#NEVER FINISHED

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
from PlotAssist import HigsPlot
import EZColors
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
InitCount = 0
Sides = int(N**(1/2))
for yPos in range(1,Sides+1):
    for xPos in range(1,Sides+1):
        theta_rng = 2*np.pi*rng.random()
        p = ParticleClass(xPos, yPos, d, m, 1, theta_rng, MainSim, InitCount)
        MainSim.Ensemble.append(p)
        InitCount+=1

MainSim.ConstructPairs()
for pairs in MainSim.Pairs:
    pairs.updateCollisionTime() #warning, some pairs will never collide
    pairs.Pair[0].updateWallCollision()
    pairs.Pair[1].updateWallCollision()

MainSim.setCollisionTimeTable()

#CHECK NO OF PAIRS PER PARTICLE
for p in MainSim.Ensemble:
    print(len(p.PairedPairs))
'''
    EQUILIBRIZATION
'''


#now all particles are ranked in order of 
#while MainSim.COLLISIONS < MainSim.MAX_COLLISIONS and MainSim.t0 < MainSim.MAXTIME:
    #Update the first element in the collision table
P = MainSim.CollisionTimeTable[0]
MainSim.CollisionObject = P
MainSim.ShortestCollision = None
if isinstance(P, ParticleClass):
    MainSim.ShortestCollision = P.WallCollisionTime
else:
    MainSim.ShortestCollision = P.Tc
MainSim.StepForward() #all particles moved and their velocities updated
#update the next Tc of this particle/pair
if isinstance(P, ParticleClass):
    P.updateWallCollision() #find the next wall collision
    for pair in P.PairedPairs:
        P.updateCollisionTime()
    #also, now 
else:
    P.updateCollisionTime() #this will be set to None, they just collided.
#now move this at the back of the list


#SANITY CHECK
for p in MainSim.CollisionTimeTable:
    if isinstance(p, ParticleClass):
        print(p.WallCollisionTime)
    else:
        print(p.Tc)

SimulationStartTime = time.time()
