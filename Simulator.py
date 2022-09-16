import numpy as np
from Particle import ParticleClass
from Pairs import PairsClass
import matplotlib.pyplot as plt

class SimulatorClass:

    def __init__(self,N, eta,):
        #Set Maximum
        self.MAX_COLLISIONS = 500
        self.COLLISIONS = 0
        self.TIMESTEP = 0.0001
        self.MAXTIME = 1000
        #Variable Definitions
        self.t0 = 0
        self.CollisionObject = None
        self.ShortestCollision = None
        #Constant Definitions
        self.N = N
        self.eta = eta
        self.L = 1

        #All Particles
        self.Ensemble = []
        self.Pairs = []

        #FullSimulation
        self.Saved = []
        #populate this with MAXCOLLISION
        for c in range(self.MAX_COLLISIONS+1):
            Xpos = np.zeros(self.N);    Ypos = np.zeros(self.N)
            Uvel = np.zeros(self.N);    Vvel = np.zeros(self.N)
            self.Saved.append([Xpos, Ypos, Uvel, Vvel])


        #each zero is a count from 0-0.05, 0.05 to 0.1
        self.BracketInterval = 0.05
        self.BracketStart, self.BracketEnd = 0,5
        self.BracketSteps = (self.BracketEnd-self.BracketStart)/self.BracketInterval
        

        self.SpeedBracketsU = np.zeros(int(self.BracketSteps))
        self.SpeedBracketsV = np.zeros(int(self.BracketSteps))
        self.SpeedBracketsC = np.zeros(int(self.BracketSteps))

        #boundary
        self.Sides = int(self.N**(1/2))
        self.Boundary = self.N**(1/2) + 1

        #Store the plotter
        self.plt = plt
        self.fig = plt.figure()
        self.ax = plt.gca()
        self.ax.set_xscale('linear')
        self.ax.set_yscale('linear')
        self.ax.minorticks_on()

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        #Plots the current moment
        self.plt.xlim([0,self.Sides+1+0.004])
        self.plt.ylim([0,self.Sides+1])
        #draw bounding boxes
        self.plt.hlines([0,self.Boundary], 0, self.Boundary, color = 'k', linewidth = 2, linestyle = '--')
        self.plt.vlines([0,self.Boundary], 0, self.Boundary, color = 'k', linewidth = 2, linestyle = '--')
        

    def ConstructPairs(self,):
        #Generate all the possible pairs
        for P1 in self.Ensemble:
            for P2 in self.Ensemble:
                if (P1 is P2): continue #skip identicals
                if self.__isAlreadyPaired(P1, P2) == True: continue #skip paired
                P1.PairedParticles.append(P2)
                P2.PairedParticles.append(P1)
                newpair = PairsClass(P1,P2, self)
                self.Pairs.append(newpair)

    def __isAlreadyPaired(self, P1, P2):
        isPaired = False
        for p in P1.PairedParticles:
            if p is P2: isPaired = True
        for p in P2.PairedParticles:
            if p is P1: isPaired = True
        return isPaired

    def Screenshot(self,):
        #Save information of ALL positions+vel at EACH time frame.
        self.__getAllPositions()
       
        
    def Movie(self,):
        for XY in self.Saved:
            X,Y = XY[0],XY[1]
            tp = self.plt.scatter(X,Y,color = 'r', s = 3)
            self.plt.pause(self.TIMESTEP)
            tp.remove()
        self.plt.show()

    def __getAllPositions(self,):
        #The following is being handled by Particle updatePosition(), hopefully
        # c = self.COLLISIONS #index 
        
        # for i in range(0,self.N):
        #     p = self.Ensemble[i]
        #     self.Saved[c][0][i] = p.R[0];  self.Saved[c][1][i] = p.R[1]
        #     self.Saved[c][2][i] = p.V[0];  self.Saved[c][3][i] = p.V[1]
        pass
        #return Xpos, Ypos, Uvel, Vvel


    def StepForward(self,):
        self.COLLISIONS = self.COLLISIONS + 1
        dt = self.ShortestCollision - self.t0

        #update the position of each particle by dt
        for p in self.Ensemble:
            p.updatePosition(dt)

        #after updating the position, check what type of collision it was
        if isinstance(self.CollisionObject, ParticleClass):
            #print("It was a particle that collided with wall!")
            #print(self.CollisionObject.WallCollisionPoint)
            CP = self.CollisionObject.WallCollisionPoint
            #This is going to be very dumb:
            if CP[0] == 0 or CP[0] == self.Boundary:
                self.CollisionObject.V[0] = -self.CollisionObject.V[0]
            if CP[1] == 0 or CP[1]== self.Boundary:
                self.CollisionObject.V[1] = -self.CollisionObject.V[1]
        else:
            #print("It was a particle that collided with another particle!")
            P1, P2 = self.CollisionObject.Pair[0], self.CollisionObject.Pair[1]
            R1, R2 = P1.getR(), P2.getR()
            V1, V2 = P1.getV(), P2.getV()
            R12 = R1 - R2 
            R12_Hat = R12 / np.linalg.norm(R12)
            NewV1 = V1 - np.dot((V1 - V2), R12_Hat) * R12_Hat
            NewV2 = V2 + np.dot((V1 - V2), R12_Hat) * R12_Hat
            P1.V = NewV1
            P2.V = NewV2
           
        #update time
        self.t0 = self.ShortestCollision

    def GenerateDistribution(self,):
        def findBracket(x):
            #print("finding bracket for ",np.abs(x))
            #i = 0 #my bracket slot
            x = np.abs(x)
            for i in range(0, int(self.BracketSteps)):
                StartRange = 0.05*i
                EndRange = 0.05*(i+1)
                if StartRange <= x and x < EndRange:
                    return i
            return None #faster than 5 unit/time
        
        for Ensemble in self.Saved:
            #0 = X, 1 = Y, 2 = U, 3 = V
            #These are the lists of u,v of every single particle
            UList,VList = Ensemble[2], Ensemble[3]
            for i in range(len(UList)):
                U,V = UList[i], VList[i]
                C =  np.sqrt(U**2 + V**2)
                #do not confuse the i subscript here with i'th iter
                # it is to say i_th "bracket"
                U_i,V_i,C_i = findBracket(U), findBracket(V), findBracket(C)
                if U_i != None:
                    self.SpeedBracketsU[U_i] = self.SpeedBracketsU[U_i] + 1

                if V_i != None:
                    self.SpeedBracketsV[V_i] = self.SpeedBracketsV[V_i] + 1
                if C_i != None:
                    self.SpeedBracketsC[C_i] = self.SpeedBracketsC[C_i] + 1
           
            #Normalize by total particles
        Normalization = self.MAX_COLLISIONS*self.N
        return self.SpeedBracketsU/Normalization, self.SpeedBracketsV/Normalization, self.SpeedBracketsC/Normalization

            
