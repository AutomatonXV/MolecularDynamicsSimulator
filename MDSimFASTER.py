#NEVER FINISHED

'''
MOLECULAR DYNAMICS SIMULATOR 
    FASTER TIME ALGORITHM
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
N = 400                             # number of particles
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

'''
    EQUILIBRIZATION
'''
print("SIMULATION HAS BEGUN.")
SimulationStartTime = time.time()

while MainSim.COLLISIONS < MainSim.MAX_COLLISIONS:
    #update the position of all particles and their velocities
    #the shortest time particles will be at the first of collision table
    MainSim.CollisionObject = MainSim.getQuickestEvent()
    MainSim.ShortestCollision = MainSim.CollisionObject.Tc
    MainSim.StepForward()
    #go through each particle and update their encounter times
    LastCollided = MainSim.CollisionObject
    MainSim.CollisionObject = None
    MainSim.ShortestCollision = None

    #update every involved particle's collision time

    def UpdateAllInvolvedPairs(LC):
        #argument is the last collided particle
        #in the case of a pair, submit both particle 0 and 1
        #one after the other
        for pair in LC.PairedPairs:
            pair.updateCollisionTime()
            #the following will stop themselves from computing
            #if we already computed for this iteration
            pair.Pair[0].updateWallCollision() 
            pair.Pair[1].updateWallCollision()

    if isinstance(LastCollided, ParticleClass):
        #if the last collided obj was a particle
        #then update every pair 
        LastCollided.updateWallCollision()
        UpdateAllInvolvedPairs(LastCollided)
    else:
        #the last collided was a pair
        #need to update the involved pairs of both of the particles
        UpdateAllInvolvedPairs(LastCollided.Pair[0])
        UpdateAllInvolvedPairs(LastCollided.Pair[1])
        pass

    CollisionPercent = MainSim.COLLISIONS/MainSim.MAX_COLLISIONS*100
    if CollisionPercent%5 == 0: 
        print("COLLISION %\t",100* MainSim.COLLISIONS/MainSim.MAX_COLLISIONS, 
        "%, \tSIM. TIME\t", MainSim.t0,
        "\t Time Elapsed: \t",time.time() - SimulationStartTime)



SimulationEndTime = time.time() 
Elapsed = SimulationEndTime - SimulationStartTime
print("TOTAL TIME ELAPSED:\t", Elapsed)


'''
    POST PROCESSING
'''
# AnimateParticles = AnimatorClass(MainSim)
# AnimateParticles.Movie()

Stats3D = AnimatorClass(MainSim)
Stats3D.StatisticsEnd2D(m,K,T)

Stats1D = AnimatorClass(MainSim)
Stats1D.StatisticsEnd1D(True, m,K,T)

# Stats1D = AnimatorClass(MainSim)
# Stats1D.StatisticsEnd1D(False,m,K,T)


# AnimateStatistics = AnimatorClass(MainSim)
# AnimateStatistics.StatisticsMovieV2(m,K,T)

# Brownian = AnimatorClass(MainSim)
# #Brownian.InitialFrame(MainSim.N)
# colorseq = [(1,0,0), (0,0,1), (0,178/255,18/255), (0.6,0.6,0.6)]
# particleseq = [0,19, N-20, N-1]
# Brownian.DrawBrownian(particleseq, colorseq)
