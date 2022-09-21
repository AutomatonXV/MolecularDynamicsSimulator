'''
MOLECULAR DYNAMICS SIMULATOR 
   STANDARD TIME ALGORITHM
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
from Animator import AnimatorClass
import time 
#################################################
'''
            PARAMETER DEFINITION
'''
#   Particle Constants
d = 0.1                             # diameter
m = 1                             # mass
K = 1
T = 1/2
V_spheres = 4/3*np.pi*(d/2)**3      # volume

#   Simulation Constants
N = 36                             # number of particles
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

SimulationStartTime = time.time()
while MainSim.COLLISIONS < MainSim.MAX_COLLISIONS and MainSim.t0 < MainSim.MAXTIME:
        #reset collision objects
        MainSim.CollisionObject = None
        MainSim.ShortestCollision = None
        OldTc = MainSim.t0
        #Check for pair collision
        for pairs in  MainSim.Pairs: 
                
                pairs.updateCollisionTime()
                #youll have to go through each particle in pair later anyway, so:
                pairs.Pair[0].updateWallCollision()
                pairs.Pair[1].updateWallCollision()
                #print(pairs.Tc)
        
        MainSim.StepForward()
        if MainSim.t0 < OldTc: break #WTF?

        CollisionPercent = MainSim.COLLISIONS/MainSim.MAX_COLLISIONS*100
        if CollisionPercent%25 == 0: 
                print("COLLISION %\t",100* MainSim.COLLISIONS/MainSim.MAX_COLLISIONS, 
                "%, \tSIM. TIME\t", MainSim.t0,
                "\t Time Elapsed: \t",time.time() - SimulationStartTime)
        
        #################################################
SimulationEndTime = time.time() 
Elapsed = SimulationEndTime - SimulationStartTime
print("TOTAL TIME ELAPSED:\t", Elapsed)


'''
        POST-PROCESSING
'''
AnimateParticles = AnimatorClass(MainSim)
AnimateParticles.Movie()

AnimateStatistics = AnimatorClass(MainSim)
AnimateStatistics.StatisticsMovie(m,K,T)


