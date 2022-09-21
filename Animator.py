import matplotlib.pyplot as plt
import numpy as np

class AnimatorClass:
    def __init__(self,Sim):
        self.Simulator = Sim
        self.MaxFrames = 100
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
        self.plt.xlim([0,self.Simulator.Sides+1+0.004])
        self.plt.ylim([0,self.Simulator.Sides+1])
        #draw bounding boxes
        self.plt.hlines([0,self.Simulator.Boundary], 0, self.Simulator.Boundary, color = 'k', linewidth = 2, linestyle = '--')
        self.plt.vlines([0,self.Simulator.Boundary], 0, self.Simulator.Boundary, color = 'k', linewidth = 2, linestyle = '--')
        

    def Movie(self,):
        for XY in self.Simulator.Saved:
            X,Y = XY[0],XY[1]
            tp = self.plt.scatter(X,Y,color = 'r', s = 3)
            self.plt.pause(self.Simulator.TIMESTEP)
            tp.remove()
        self.plt.show()

    def StatisticsMovie(self,m,K,T):
        #Plots the current moment
        self.plt.xlim([0,5])
        self.plt.ylim([0,1])
        self.plt.xlabel("Speed")
        self.plt.ylabel("X(C)")

        F_Cx, F_Cy, C = self.Simulator.GenerateDistribution(m,K,T)
        MaxWellRange = np.linspace(0,5,100)
        MaxwellFunc = self.Simulator.MaxWell2D(MaxWellRange, m, K,T)
        Speed = np.arange(self.Simulator.BracketStart, self.Simulator.BracketEnd, self.Simulator.BracketInterval)
        self.plt.plot(MaxWellRange, MaxwellFunc, color = 'r')

        i = 0
        clr = (0/255, 0/255, 0/255)

        AllFrames = []
        FrameStep = int(np.floor(len(self.Simulator.Historic)/self.MaxFrames))
        for f in range(0, self.MaxFrames):
            AllFrames.append(self.Simulator.Historic[f*FrameStep])
            print("end on frame", f*FrameStep, len(self.Simulator.Historic))

        for lines in AllFrames:
            tp = self.plt.plot(Speed, lines, color = clr, markersize = 0.3, )
            self.plt.pause(self.Simulator.TIMESTEP)
            if i < len(AllFrames):
                tpremoved = tp.pop(0)
                tpremoved.remove()
            i +=1
        self.plt.plot(Speed, C, color = clr, markersize = 0.3)
        self.plt.show()

