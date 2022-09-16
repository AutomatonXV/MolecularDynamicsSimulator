import numpy as np

class PairsClass:
    def __init__(self, P1,P2, Simulator):
        self.Simulator = Simulator
        self.Pair = [P1,P2]
        self.Tc = None #collision time

    def setSimulatorShortest(self,):
        self.Simulator.ShortestCollision = self.Tc
        self.Simulator.CollisionObject = self

    def updateCollisionTime(self,):
        R12 = self.__getR12()
        V12 = self.__getV12()
        t0 = self.Simulator.t0
        sigma = self.Pair[0].d
        
        DOTV12R12 = np.dot(V12, R12)
        V12Squared = np.dot(V12,V12)
        R12Squared = np.dot(R12,R12)
        Discriminant = np.sqrt( DOTV12R12**2 - V12Squared * (R12Squared - sigma) )
        #negative sign is physically possible. Discard other one.
        PastTc = t0
        result1 = (-DOTV12R12 - Discriminant)/(V12Squared)
        result2 = (-DOTV12R12 + Discriminant)/(V12Squared)
        if result1 > 0:
            self.Tc = t0 + result1
        else:
            self.Tc = t0 + result2
        # if self.Tc < PastTc: 
        #         # print("FATAL TIME ERROR: PAIR COLLISION", PastTc, self.Tc, self.Tc - PastTc)
        #         # print(R12, V12, Discriminant)
        #         # print((-DOTV12R12 - Discriminant)/(V12Squared))
        #         # print( (-DOTV12R12 + Discriminant)/(V12Squared))
        if not self.Simulator.ShortestCollision: self.setSimulatorShortest(); return
        if self.Simulator.ShortestCollision > self.Tc: self.setSimulatorShortest(); return
        return 
        
    def isApproaching(self,):
        R12 = self.__getR12()
        V12 = self.__getV12()
        if np.dot(V12, R12) < 0: return True
        return False
    
    def isColliding(self,):
        sigma = self.Pair[0].d
        R12 = self.__getR12()
        V12 = self.__getV12()
        R12Squared = np.dot(R12,R12)
        V12Squared = np.dot(V12,V12)
        DOTPROD = np.dot(V12, R12)**2
        SUBTRACT = V12Squared * (R12Squared - sigma**2)
        if (DOTPROD - SUBTRACT) >= 0: return True
        return False

    def __getR12(self,):
        R1 = self.Pair[0].getR()
        R2 = self.Pair[1].getR()
        return (R1-R2)
    
    def __getV12(self,):
        V1 = self.Pair[0].getV()
        V2 = self.Pair[1].getV()
        #print("Velocities","\t",V1,"\t", V2)
        return (V1-V2)

    