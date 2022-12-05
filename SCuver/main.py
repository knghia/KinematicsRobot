import numpy as np
PI = np.pi
import matplotlib.pyplot as plt

class SCuver:
    def __init__(self,f,z,r):
        self.k1 = z/(PI*f)
        self.k2 = 1/((2*PI*f)*(2*PI*f))
        self.k3 = r*z/(2*PI*f)
        self.T = 0.0
        
        self.xp = 0
        self.y = 0
        self.yd = 0

    def upload(self, x):
        xd = (x- self.xp)/self.T
        self.xp  = x
        self.y = self.y+ self.T*self.yd
        self.yd = self.yd + self.T*(x+ self.k3*xd- self.y- self.k1*self.yd)/self.k2
        return self.y
    
scuver = SCuver(f=0.5,z=0.15,r=0)

x = np.linspace(0,10,10000)
y = [scuver.upload(i) for i in x]

plt.plot(x,y)
plt.show()
