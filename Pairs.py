import numpy as np

class PairsClass:
    def __init__(self, P1,P2, Simulator):
        self.Simulator = Simulator
        self.Pair = [P1,P2]
        self.Tc = None #collision time
        #
        self.Pair[0].PairedPairs.append(self)
        self.Pair[1].PairedPairs.append(self)

    def setSimulatorShortest(self,):
        self.Simulator.ShortestCollision = self.Tc
        self.Simulator.CollisionObject = self

    def updateCollisionTime(self,):
        t0 = self.Simulator.t0
        #condition 1: on approach
        sigma = self.Pair[0].d
        R12 = self.__getR12()
        V12 = self.__getV12()
        DOTV12R12 = np.dot(V12, R12)
        if DOTV12R12 >= 0: return False #no collision, return false

        #condition 2: now on approach
        R12Squared = np.dot(R12,R12)
        V12Squared = np.dot(V12,V12)
        DOTPROD = DOTV12R12**2
        SUBTRACT = V12Squared * (R12Squared - sigma**2)
        if (DOTPROD - SUBTRACT) < 0: return False #no collision, return false
        
        #condition 3: now on collision course.
        Discriminant = np.sqrt( DOTV12R12**2 - SUBTRACT )
        #negative sign is physically possible. Discard other one.
        result1 = (-DOTV12R12 - Discriminant)/(V12Squared)
        result2 = (-DOTV12R12 + Discriminant)/(V12Squared)
        if result1 > 0:
            self.Tc = t0 + result1
        else:
            self.Tc = t0 + result2
        # if self.Tc < PastTc: 
        #         # print("FATAL TIME ERROR: PAIR COLLISION", t0, self.Tc, self.Tc - PastTc)
        #         # print(R12, V12, Discriminant)
        #         # print((-DOTV12R12 - Discriminant)/(V12Squared))
        #         # print( (-DOTV12R12 + Discriminant)/(V12Squared))

        #Set if shortest time
        if not self.Simulator.ShortestCollision: self.setSimulatorShortest(); return True
        if self.Simulator.ShortestCollision > self.Tc: self.setSimulatorShortest(); return True
        return True #last return statement
        
    # def isApproaching(self,):
    #     sigma = self.Pair[0].d
    #     R12 = self.__getR12()
    #     V12 = self.__getV12()
    #     if np.dot(V12, R12) < 0: return True
    #     #condition 2
    #     R12Squared = np.dot(R12,R12)
    #     V12Squared = np.dot(V12,V12)
    #     DOTPROD = np.dot(V12, R12)**2
    #     SUBTRACT = V12Squared * (R12Squared - sigma**2)
    #     if (DOTPROD - SUBTRACT) >= 0: return True
    #     return False
    
    # def isColliding(self,):
    #     sigma = self.Pair[0].d
    #     R12 = self.__getR12()
    #     V12 = self.__getV12()
    #     R12Squared = np.dot(R12,R12)
    #     V12Squared = np.dot(V12,V12)
    #     DOTPROD = np.dot(V12, R12)**2
    #     SUBTRACT = V12Squared * (R12Squared - sigma**2)
    #     if (DOTPROD - SUBTRACT) >= 0: return True
    #     return False

    def __getR12(self,):
        R1 = self.Pair[0].getR()
        R2 = self.Pair[1].getR()
        return (R1-R2)
    
    def __getV12(self,):
        V1 = self.Pair[0].getV()
        V2 = self.Pair[1].getV()
        #print("Velocities","\t",V1,"\t", V2)
        return (V1-V2)

    