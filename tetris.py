import time
import os
import sys
from pynput import keyboard
class tetris:
#create the figures
    rows,cols=(22,10*2)
    def __init__(self):
        self.velocity=2 # 2 sec
        self.figureN=0
        self.figPos=1
        if os.name == "posix":
            self.var = "clear"       
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            self.var = "cls"
        
        line=["[][][][]","""[]\n[]\n[]\n[]"""]
        self.base=[]
        for x in range(20):
            self.base.append((-1,x))
        self.center=[22,11]
        self.figure=[]
        figureN=[]
        for x in line:
            figureN.append(self.extractFigure(x))
        self.figure.append(figureN)
        listener = keyboard.Listener(on_press=self.pressKey)
        listener.start()
        self.timeEjecution()
    
    def extractFigure(self,f):
        data=f.split("\n")
        listx=[]
        for x in data:
            listy=[]
            for y in x:
                listy.append(y)
            listx.append(listy)
        return listx 
    
    def timeEjecution(self):
        
        while 1:
            time.sleep(0.2)
            self.failPiece(self.figure,self.center)
              
    def pressKey(self,key):
        temp=self.figPos
        if key==keyboard.Key.up:
            temp+=1
            temp=temp%len(self.figure[self.figureN])
            if self.compareBoundaries(temp,False):
                self.figPos=temp
                if self.center[1]%2==0:
                    self.center[1]+=1
                else:
                    self.center[1]-=1
            
        temp=self.center[1]
        if key== keyboard.Key.right:
            temp+=2
            
        if key==keyboard.Key.left:
            temp-=2
        if self.controlColision(temp): 
            self.center[1]=self.compareBoundaries(temp,True)
        
    def compareBoundaries(self,temp,flag):
        if flag:
            lx=len(self.figure[self.figureN][self.figPos][0])
            centX=temp
            v1=int(lx/2)+centX>self.cols
            v2=centX-int(lx/2)<0
            if not( v2 or v1):
                centX=temp
            else:       
                centX=self.center[1]
            return centX
                
               
        else:
            lx=len(self.figure[self.figureN][temp][0])
            centX=self.center[1]
            
            v1=int(lx/2)+centX>self.cols
            v2=centX-int(lx/2)<0
            return not( v2 or v1)
            
    def controlColision(self,temp):
        figureDimension=[len(self.figure[self.figureN][self.figPos]),len(self.figure[self.figureN][self.figPos][0])]
        halfD=[figureDimension[0]/2,figureDimension[1]/2]
        initx=int(self.center[0]-halfD[0])
        inity=int(temp-halfD[1])
        valBool=True
        fg=self.figure[self.figureN][self.figPos]
        for x in range(figureDimension[0]):
            for y in range(figureDimension[1]):
                if (initx+x,inity+y) in self.base and fg[x][y]!='.':
                    valBool=False
                    break 
        return valBool   
        
    def deleteColumn(self):
        baseL=self.base
        baseL.sort()
        cont=0
        contDelLines=0
        va=0
        baseA=[]
        baseB=[]
        baseC=[]
        for x in baseL:
            y,z=x
            baseA.append((y-contDelLines,z))
            if y !=-1 :
                if va==y-contDelLines:
                    cont+=1
                    if cont==20:
                        contDelLines+=1
                        baseA=[]
                else:
                    baseB.extend(baseA)
                    baseA=[]
                    cont=1
                    va=y-contDelLines
            else:
                baseB.extend(baseA)
                baseA=[]
                
            
        if cont!=20:
            baseB.extend(baseA)
            baseA=[]
                
        self.base=baseB


     

    def failPiece(self,f,center):
        
        if self.controlFail():
            center[0]-=1
        else:
            
            self.nextFigure()
            self.deleteColumn()
        self.drawScreen(f,center)
        
    def controlFail(self):
        figureDimension=[len(self.figure[self.figureN][self.figPos]),len(self.figure[self.figureN][self.figPos][0])]
        halfD=[figureDimension[0]/2,figureDimension[1]/2]
        initx=int(self.center[0]-halfD[0])
        inity=int(self.center[1]-halfD[1])
        valBool=True
        fg=self.figure[self.figureN][self.figPos]
        for x in range(figureDimension[0]):
            for y in range(figureDimension[1]):
                if (initx+x-1,inity+y) in self.base and fg[x][y]!='.':
                    valBool=False
                    break 
        return valBool
    
    def nextFigure(self):
        figure=self.figure[self.figureN][self.figPos]
        figureDimension=[len(figure),len(figure[0])]
        halfD=[figureDimension[0]/2,figureDimension[1]/2]
        initx=int(self.center[0]-halfD[0])
        inity=int(self.center[1]-halfD[1])
        for x in range(figureDimension[0]):
            for y in range(figureDimension[1]):
                fg=figure
                if fg[x][y]!='.':
                    try:
                        self.base.append((initx+x,inity+y))
                    except:
                        ls="no hacer nada"
        
        self.figPos=1
        self.figureN=0
        self.center=[22,11]
    
    def drawScreen(self,figure,center):
        os.system(self.var)
        
        grid=[]
        for x in range(self.rows): 
            gridx=[]
            for y in range(self.cols): gridx.append(".")
            grid.append(gridx)
        figureDimension=[len(figure[self.figureN][self.figPos]),len(figure[self.figureN][self.figPos][0])]
        halfD=[figureDimension[0]/2,figureDimension[1]/2]
        initx=int(center[0]-halfD[0])
        inity=int(center[1]-halfD[1])
        for x in range(figureDimension[0]):
            for y in range(figureDimension[1]):
                fg=figure[self.figureN][self.figPos]
                if fg[x][y]!='.':
                    try:
                        grid[initx+x][inity+y]=fg[x][y]
                    except:
                        ls="no hacer nada"
        for x in self.base:
            y,z=x
            if y!=-1:
                if z%2==0:
                    grid[y][z]='['
                else:
                    grid[y][z]=']'           
        #print all
        grid=grid[::-1]
        for x in grid:
            print("".join(x))
            
        
        
        
            
        
    
        

    
tetris()