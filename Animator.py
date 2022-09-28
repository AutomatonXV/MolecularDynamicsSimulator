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

        

    def Movie(self,):
        #draw bounding boxes
        self.plt.hlines([0,self.Simulator.Boundary], 0, self.Simulator.Boundary, color = 'k', linewidth = 2, linestyle = '--')
        self.plt.vlines([0,self.Simulator.Boundary], 0, self.Simulator.Boundary, color = 'k', linewidth = 2, linestyle = '--')
        for XY in self.Simulator.Saved:
            X,Y = XY[0],XY[1]
            tp = self.plt.scatter(X,Y,color = 'r', s = 3)
            self.plt.pause(self.Simulator.TIMESTEP)
            tp.remove()
        self.plt.show()

    def getHisto(self, C, Speeds):
        #go through the list c, then 
        mult = (C)
        freq = []
        for x in mult:
            #print(x)
            #print(mult)
            for n in range(0, int(x)):
                freq.append(x)
        return freq
        pass

    def StatisticsEnd1D(self, U, m, K, T):
        self.plt.xlim([-2,2])
        self.plt.ylim([0,1])
        self.plt.xlabel("Speed (Unit/Time)")
        self.plt.ylabel("f(C)")

        UHisto, VHisto, CHisto = self.Simulator.getRaw()
        MaxWellRange = np.linspace(-5,5,200)
        MaxwellFunc = self.Simulator.MaxWell1D(MaxWellRange, m, K,T)
        Speed = np.arange(-self.Simulator.BracketEnd, self.Simulator.BracketEnd, self.Simulator.BracketInterval)
        self.plt.plot(MaxWellRange, MaxwellFunc, color = 'r')
        if U == True:
            self.plt.hist(UHisto, bins = Speed, density= True)#Speed)
        else:
            self.plt.hist(VHisto, bins = Speed, density= True)#Speed)
        self.plt.show()

    def StatisticsEnd2D(self,m,K,T):
        self.plt.xlim([0,5])
        self.plt.ylim([0,1])
        self.plt.xlabel("Speed (Unit/Time)")
        self.plt.ylabel("X(C)")

        UHisto, VHisto, CHisto = self.Simulator.getRaw()
        MaxWellRange = np.linspace(0,5,100)
        MaxwellFunc = self.Simulator.MaxWell2D(MaxWellRange, m, K,T)
        Speed = np.arange(self.Simulator.BracketStart, self.Simulator.BracketEnd, self.Simulator.BracketInterval)
        self.plt.plot(MaxWellRange, MaxwellFunc, color = 'r')
        self.plt.hist(CHisto, bins = Speed, density= True)#Speed)
        self.plt.show()

    def InitialFrame(self, N):
        Sides = int(N**(1/2))
        for yPos in range(1,Sides+1):
            for xPos in range(1,Sides+1):
                plt.scatter(xPos, yPos, s = 3, color = 'r')
                
    def getStartingPos(self, n):
        Sides = int(self.Simulator.N**(1/2))
        count = 0
        for yPos in range(1, Sides+1):
            for xPos in range(1,Sides+1):
                if count == n: return xPos,yPos
                count = count+1

    def DrawBrownian(self, pNo, colorlist):
        #pNo is a list of numbers for particles
        MyPositions = [] #this list contains XY pos for each particle, so
        #[ [XYlist for P1] [XYlist for P2] etc]

        indeks = 0
        for i in pNo:
            listofPosX = []
            listofPosY = []
            startX,startY = self.getStartingPos(i)
            listofPosX.append(startX)
            listofPosY.append(startY)
            for XY in self.Simulator.Saved:
                X,Y = XY[0],XY[1]
                myX,myY = X[i], Y[i]
                if myX == 0 and myY == 0: continue
                listofPosX.append(myX)
                listofPosY.append(myY)
                # tp = self.plt.scatter(X,Y,color = 'r', s = 3)
                # self.plt.pause(self.Simulator.TIMESTEP)
                # tp.remove()
            XYList = [listofPosX, listofPosY]
            MyPositions.append(XYList)
        indeks = 0
        for XY_i in MyPositions:
            clr = colorlist[indeks] 
            self.plt.plot(XY_i[0],XY_i[1], linestyle = 'dashed', marker = 'o', markersize = 3, color = clr)
            indeks +=1
        self.plt.show()   

    def StatisticsMovieV2(self,m,K,T):
        #Version 2
        self.plt.xlim([0,5])
        self.plt.ylim([0,1])
        self.plt.xlabel("Speed")
        self.plt.ylabel("X(C)")

        self.Simulator.generateHistoric(m,K,T)

        MaxWellRange = np.linspace(0,5,100)
        MaxwellFunc = self.Simulator.MaxWell2D(MaxWellRange, m, K,T)
        Speed = np.arange(self.Simulator.BracketStart, self.Simulator.BracketEnd, self.Simulator.BracketInterval)
        self.plt.plot(MaxWellRange, MaxwellFunc, color = 'r')

        i = 0
        AllFrames = []
        FrameStep = int(np.floor(len(self.Simulator.Historic)/self.MaxFrames))
        for f in range(0, self.MaxFrames):
            AllFrames.append(self.Simulator.Historic[f*FrameStep])
            print("end on frame", f*FrameStep, len(self.Simulator.Historic))

        for lines in AllFrames:
            counts,bins,bars = self.plt.hist(lines, bins = Speed,density= True, color = (0/255, 0/255, 0/255) )
            self.plt.pause(self.Simulator.TIMESTEP)
            if i < len(AllFrames)-1:
                [b.remove() for b in bars]
                # tpremoved = tp.pop(0)
                # tpremoved.remove()
            i +=1

        self.plt.show()

    # #DEPRECATED
    # def StatisticsMovie(self,m,K,T):
    #     #Plots the current moment
    #     self.plt.xlim([0,5])
    #     self.plt.ylim([0,1])
    #     self.plt.xlabel("Speed")
    #     self.plt.ylabel("X(C)")

    #     F_Cx, F_Cy, C = self.Simulator.GenerateDistribution(m,K,T)
    #     MaxWellRange = np.linspace(0,5,100)
    #     MaxwellFunc = self.Simulator.MaxWell2D(MaxWellRange, m, K,T)
    #     Speed = np.arange(self.Simulator.BracketStart, self.Simulator.BracketEnd, self.Simulator.BracketInterval)
    #     self.plt.plot(MaxWellRange, MaxwellFunc, color = 'r')

    #     i = 0
    #     clr = (0/255, 0/255, 0/255)

    #     AllFrames = []
    #     FrameStep = int(np.floor(len(self.Simulator.Historic)/self.MaxFrames))
    #     for f in range(0, self.MaxFrames):
    #         AllFrames.append(self.Simulator.Historic[f*FrameStep])
    #         print("end on frame", f*FrameStep, len(self.Simulator.Historic))

    #     for lines in AllFrames:
    #         tp = self.plt.plot(Speed, lines, color = clr, markersize = 0.3, )
    #         self.plt.pause(self.Simulator.TIMESTEP)
    #         if i < len(AllFrames)-1:
    #             tpremoved = tp.pop(0)
    #             tpremoved.remove()
    #         i +=1
    #     #self.plt.plot(Speed, C, color = clr, markersize = 0.3)
    #     self.plt.show()

