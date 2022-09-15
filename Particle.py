import numpy as np

class ParticleClass:

    def __init__(self, PosX, PosY, Diam, Mass, VelMag, Theta,Simulator):
        #override for testing
        #Theta = np.deg2rad(30)
        #Particle Variables
        self.X = PosX
        self.Y = PosY
        self.U = VelMag * np.cos((Theta))
        self.V = VelMag * np.sin((Theta))
        #Particle Constants
        self.d = Diam
        self.m = Mass
        self.T = 1/2
        self.K = 1

        #Store Simulation
        self.Simulator = Simulator

        #Store pairs
        self.PairedParticles = []

        #Variables
        self.WallCollisionTime = None #default
        self.WallCollisionPoint = None

    def getR(self,):
        #convert XY into vector
        return np.array([self.X, self.Y])

    def getV(self,):
        #convert XY into vector
        return np.array([self.U, self.V])

    def setSimulatorShortest(self,):
        self.Simulator.ShortestCollision = self.WallCollisionTime
        self.Simulator.CollisionObject = self

    def updatePosition(self,dt):
        r = self.getR()
        v = self.getV()
        r1 = r + v*dt
        self.X = r1[0]
        self.Y = r1[1]

    def updateWallCollision(self,):
        #the general idea is find the intersection of 2 vector lines
        #then create the intersection as an imaginary particle
        #then see if our particle is approaching said particle
        #then calculate closest time
        Rx = self.X ; Ry = self.Y ; Vx = self.U ; Vy = self.V 
        X1 = self.Simulator.Boundary ; Y1 = self.Simulator.Boundary
        #the equation for our particle is:
        # (Rx, Ry) + (Vx, Vy)S
        #The equation for left side wall is:
        # (0,0) + (0,y1)T
        #The equation for right side wall is:
        # (x0,0) + (0,y1)T
        #The equation for bottom side wall is:
        # (0,0) + (X1,0)T
        #The equation for top side wall is:
        # (0,Y1) + (X1,0)T

        #SOLVE ALL 4 WALL COLLISION SPOTS
        #for the left side wall
        T_left = 1/Y1 * (Ry - Vy * (Rx / Vx))
        T_right = 1/Y1 * (Ry + Vy * (X1 - Rx)/Vx)
        T_bottom = 1/X1 * (Rx - Vx * (Ry / Vy))
        T_top = 1/X1 * (Rx + Vx * (Y1 - Ry)/Vy)
        #write positions
        Pos_left = np.array([0,Y1 * T_left])
        Pos_right = np.array([X1,Y1 * T_right])
        Pos_bottom = np.array([X1 * T_bottom,0])
        Pos_top = np.array([X1 * T_top,Y1])
        AllPos = [Pos_left, Pos_right, Pos_bottom, Pos_top]
        
        #print(AllPos)
        self.WallCollisionTime = 10**10
        self.WallCollisionPoint = None

        for pos in AllPos:
            #Condition 1: check if they hit WITHIN the boundaries:
            # the particles may have found an intersection that is outside box. Discard.
            if pos[0] < 0 or pos[0] > X1: continue
            if pos[1] < 0 or pos[1] > Y1: continue
            
            R12 = self.getR() - pos
            V12 = self.getV() - np.array([0,0])
            V12R12SQUARED = np.dot(V12,R12)**2
            V12SQUARED = np.dot(V12,V12)
            R12SQUARED = np.dot(R12,R12)
            sigmaSQUARED = self.d**2
            Determinant = V12R12SQUARED - V12SQUARED*(R12SQUARED-sigmaSQUARED)

            #Condition 2: check if apporaching
            if np.dot(V12,R12) >=0: continue

            #Condition 3: Must collide
            if (Determinant) <0: continue
            t0 = self.Simulator.t0
            tc = t0 + ( (-np.dot(V12,R12)) - np.sqrt(Determinant)  )/V12SQUARED

            self.WallCollisionPoint = pos
            self.WallCollisionTime = tc
            # print("APPROACH",self.getR(), self.getV(), pos)
            #print("COLLISION WITH WALL", tc, pos)
        
        #check if this is the shortest event so far
        if not self.Simulator.ShortestCollision: self.setSimulatorShortest(); return
        if self.Simulator.ShortestCollision > self.WallCollisionTime: self.setSimulatorShortest(); return
        return 



