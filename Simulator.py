import numpy as np
from Particle import ParticleClass
import matplotlib.pyplot as plt

class SimulatorClass:

    def __init__(self,N, eta,):
        #Constant Definitions
        self.N = N
        self.eta = eta
        self.L = 1

        #All Particles
        self.Ensemble = []
        self.Sides = int(self.N**(1/2))

        #Store the plotter
        self.plt = plt
        self.fig = plt.figure()
        self.ax = plt.gca()
        self.ax.set_xscale('linear')
        self.ax.set_yscale('linear')
        self.ax.minorticks_on()

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def Screenshot(self,):
        #Plots the current moment
        plt.xlim([0,self.Sides+1])
        plt.ylim([0,self.Sides+1])
        X,Y = self.__getAllPositions()
        plt.scatter(X,Y, color = 'k', s = 0.1)
        plt.show()

    def __getAllPositions(self,):
        Xpos = np.zeros(self.N)
        Ypos = np.zeros(self.N)
        for i in range(0,self.N):
            p = self.Ensemble[i]
            Xpos[i] = p.X
            Ypos[i] = p.Y

        return Xpos, Ypos


