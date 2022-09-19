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
from PlotAssist import HigsPlot
import EZColors
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
N = 128                             # number of particles
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
# #CHECK NO OF PAIRS PER PARTICLE
# for p in MainSim.Ensemble:
#     print(len(p.PairedPairs))
'''
    EQUILIBRIZATION
'''

# #SANITY CHECK
# for p in MainSim.CollisionTimeTable:
#     if isinstance(p, ParticleClass):
#         print(p.WallCollisionTime)
#     else:
#         print(p.Tc)
# exit()
SimulationStartTime = time.time()
#now all particles are ranked in order of 
#while MainSim.COLLISIONS < MainSim.MAX_COLLISIONS and MainSim.t0 < MainSim.MAXTIME:
    #Update the first element in the collision table
#Times, Objects = MainSim.setCollisionTimeTable()

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

    #sort the collision time table
    #MainSim.sortCollisionTimeTable()

    CollisionPercent = MainSim.COLLISIONS/MainSim.MAX_COLLISIONS*100
    if CollisionPercent%25 == 0: 
        print("COLLISION %\t",100* MainSim.COLLISIONS/MainSim.MAX_COLLISIONS, 
        "%, \tSIM. TIME\t", MainSim.t0,
        "\t Time Elapsed: \t",time.time() - SimulationStartTime)



# #update the next Tc of this particle/pair
# if isinstance(P, ParticleClass):
#     P.updateWallCollision() #find the next wall collision
#     for pair in P.PairedPairs:
#         P.updateCollisionTime()
#     #also, now 
# else:
#     P.updateCollisionTime() #this will be set to None, they just collided.
#now move this at the back of the list


SimulationEndTime = time.time() 
Elapsed = SimulationEndTime - SimulationStartTime
print("TOTAL TIME ELAPSED:\t", Elapsed)

MainSim.Movie()

F_Cx, F_Cy, C = MainSim.GenerateDistribution(m,K,T)
MaxWellRange = np.linspace(0,5,100)
MaxwellFunc = MainSim.MaxWell2D(MaxWellRange, m, K,T)
Speed = np.arange(MainSim.BracketStart, MainSim.BracketEnd, MainSim.BracketInterval)

HPlot = HigsPlot()
Clr1 = EZColors.CustomColors(colorLabel = 'red')
Clr2 = EZColors.CustomColors(colorLabel = 'blue')
Clr3 = EZColors.CustomColors(colorLabel = 'black')
HPlot.AxLabels(X = "Speeds", Y = "f(C)")
#HPlot.SetTicks('Y',0.0,1,0.2)
HPlot.SetLim(Left = 0, Right = 5, Top = 1, Bottom = 0)
#HPlot.SetTicks('Y',1,11,1)
#HPlot.Plot((Speed, F_Cx), Color = Clr1)
#HPlot.Plot((Speed, F_Cy), Color = Clr2)
#HPlot.Plot((Speed, C), Color = Clr3)
HPlot.Plot((MaxWellRange, MaxwellFunc), Color = Clr1)
#HPlot.plt.axvline(x=FlightTime, color = 'k', linestyle = '--')
HPlot.Finalize()
HPlot.Show()



