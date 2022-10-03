import numpy as np
from Particle import ParticleClass
from Pairs import PairsClass
import matplotlib.pyplot as plt

class SimulatorClass:

    def __init__(self,N, eta,):
        #Set Maximum
        self.MAX_COLLISIONS =60000
        self.RELAX_PERCENT =  10/100
        self.RELAX_COLLISIONS = self.MAX_COLLISIONS*self.RELAX_PERCENT
        self.COLLISIONS = 0
        self.TIMESTEP = 0.00001
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
        #For ranking purposes acccording to time of collision
        self.CollisionTimeTable = []

        #FullSimulation
        self.Saved = []
        self.RawU, self.RawV, self.RawC = [],[],[] #for histogramming
        #populate this with MAXCOLLISION
        for c in range(self.MAX_COLLISIONS+1):
            Xpos = np.zeros(self.N);    Ypos = np.zeros(self.N)
            Uvel = np.zeros(self.N);    Vvel = np.zeros(self.N)
            self.Saved.append([Xpos, Ypos, Uvel, Vvel])
        self.Historic = []


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


    def StepForward(self,):
        self.COLLISIONS = self.COLLISIONS + 1
        dt = self.ShortestCollision - self.t0

        #update the position of each particle by dt
        for p in self.Ensemble:
            p.updatePosition(dt)

        #after updating the position, check what type of collision it was
        if isinstance(self.CollisionObject, ParticleClass):
            CP = self.CollisionObject.WallCollisionPoint
            #This is going to be very dumb:
            if CP[0] == 0 or CP[0] == self.Boundary:
                self.CollisionObject.V[0] = -self.CollisionObject.V[0]
            if CP[1] == 0 or CP[1]== self.Boundary:
                self.CollisionObject.V[1] = -self.CollisionObject.V[1]
        else:
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


    def setCollisionTimeTable(self,):
        #now that all the particles and pairs have tc, rank them.
        for p in self.Pairs:
            self.CollisionTimeTable.append(p)
        for p in self.Ensemble:
            self.CollisionTimeTable.append(p)

    def getQuickestEvent(self,):
        t = 10**10
        obj = None
        for p in self.CollisionTimeTable:
            if p.Tc < t:
                t = p.Tc
                obj = p
        return obj
        
   
    def printCTT(self):
        #prints all particle times as sanity check, up to Nth particle
        timetable = []
        for p in self.CollisionTimeTable:
            timetable.append(p.Tc)
        print(timetable)
        
    def MaxWell2D(self,C, m, K, T):
        A = (m/(K*T))
        B = (-m/(2*K*T))
        return A * C * np.exp(B * C**2)
    
    def MaxWell1D(self, C, m, K, T):
        A = m/(2*np.pi*K*T)
        B = (-m/(2*K*T))
        return (A ** (1/2) ) * np.exp(B*C**2)

    def getRaw(self, ):
        Utbl,Vtbl,Ctbl = [],[],[]
        CurrentEnsemble = 0
        for Ensemble in self.Saved:
            CurrentEnsemble = CurrentEnsemble + 1
            UList,VList = Ensemble[2], Ensemble[3]
            if CurrentEnsemble <= self.RELAX_COLLISIONS: continue

            for i in range(len(UList)):
                U,V = UList[i], VList[i]
                C =  np.sqrt(U**2 + V**2)
                Utbl.append(U); Vtbl.append(V); Ctbl.append(C)
        self.RawU, self.RawV, self.RawC = Utbl, Vtbl, Ctbl
        return Utbl, Vtbl, Ctbl

    def generateHistoric(self, m,K,T):
        CurrentEnsemble = 0
        for Ensemble in self.Saved:
            CurrentEnsemble = CurrentEnsemble + 1
            if CurrentEnsemble <= self.RELAX_COLLISIONS: continue
            UList, VList = Ensemble[2], Ensemble[3]
            CCount = []
            for i in range(len(UList)):
                U,V = UList[i], VList[i]
                C =  np.sqrt(U**2 + V**2)
                CCount.append(C)
            self.Historic.append(CCount)
#DEPRECATED METHODS
    # def GenerateDistribution(self,m,K,T):
    #     def findBracket(x):
    #         x = np.abs(x)
    #         for i in range(0, int(self.BracketSteps)):
    #             StartRange = 0.05*i
    #             EndRange = 0.05*(i+1)
    #             if StartRange <= x and x < EndRange:
    #                 return i
    #         return None #faster than 5 unit/time
        
    #     CurrentEnsemble = 0
    #     for Ensemble in self.Saved:
    #         CurrentEnsemble = CurrentEnsemble + 1
    #         #0 = X, 1 = Y, 2 = U, 3 = V
    #         #These are the lists of u,v of every single particle
    #         UList,VList = Ensemble[2], Ensemble[3]
    #         if CurrentEnsemble <= self.RELAX_COLLISIONS: continue

    #         for i in range(len(UList)):
    #             U,V = UList[i], VList[i]
    #             C =  np.sqrt(U**2 + V**2)
    #             #do not confuse the i subscript here with i'th iter
    #             # it is to say i_th "bracket"
    #             U_i,V_i,C_i = findBracket(U), findBracket(V), findBracket(C)
    #             if U_i != None:
    #                 self.SpeedBracketsU[U_i] = self.SpeedBracketsU[U_i] + 1

    #             if V_i != None:
    #                 self.SpeedBracketsV[V_i] = self.SpeedBracketsV[V_i] + 1
    #             if C_i != None:
    #                 self.SpeedBracketsC[C_i] = self.SpeedBracketsC[C_i] + 1
    #         #print("Are we reaching this line?")
    #         #this is to save at each step
    #         Division = CurrentEnsemble*self.N*self.BracketInterval
    #         self.Historic.append(self.SpeedBracketsC/(Division))
    #         #self.HistoricX.append(self.SpeedBracketsU/(Division))
    #         #self.HistoricY.append(self.SpeedBracketsV/(Division))
        
    #     #Normalize by total particles
    #     #this is to save overall
    #     Normalization = self.MAX_COLLISIONS*self.N*self.BracketInterval
    #     U,V,C = self.SpeedBracketsU/Normalization, self.SpeedBracketsV/Normalization, self.SpeedBracketsC/Normalization
    
    #     return U,V,C#self.MaxWell2D(C,m,K,T)


   