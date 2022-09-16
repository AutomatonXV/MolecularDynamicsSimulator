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

SimulationStartTime = time.time()
MainSim.Screenshot()
while MainSim.COLLISIONS < MainSim.MAX_COLLISIONS and MainSim.t0 < MainSim.MAXTIME:
        #reset collision objects
        MainSim.CollisionObject = None
        MainSim.ShortestCollision = None
        OldTc = MainSim.t0
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
        if MainSim.t0 < OldTc: break #WTF?

        CollisionPercent = MainSim.COLLISIONS/MainSim.MAX_COLLISIONS*100
        if CollisionPercent%5 == 0: 
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

#MainSim.Movie()


F_Cx, F_Cy, C = MainSim.GenerateDistribution()
Speed = np.arange(MainSim.BracketStart, MainSim.BracketEnd, MainSim.BracketInterval)

HPlot = HigsPlot()
Clr1 = EZColors.CustomColors(colorLabel = 'red')
Clr2 = EZColors.CustomColors(colorLabel = 'blue')
Clr3 = EZColors.CustomColors(colorLabel = 'black')
HPlot.AxLabels(X = "Speeds", Y = "f(C)")
#HPlot.SetTicks('Y',0.0,1,0.2)
HPlot.SetLim(Left = 0, Right = 5, Top = 1, Bottom = 0)
#HPlot.SetTicks('Y',1,11,1)
HPlot.Plot((Speed, F_Cx), Color = Clr1)
HPlot.Plot((Speed, F_Cy), Color = Clr2)
HPlot.Plot((Speed, C), Color = Clr3)
#HPlot.plt.axvline(x=FlightTime, color = 'k', linestyle = '--')
HPlot.Finalize()
HPlot.Show()
