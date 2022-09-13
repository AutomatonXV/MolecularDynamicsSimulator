import numpy as np

class ParticleClass:

    def __init__(self, PosX, PosY, Diam, Mass, VelMag, Theta):
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