import math
import numpy as np
import matplotlib.pyplot as plt

Ra = 2
La = 0.23
Jm = 0.000052
Bm = 0.01
Kt = 0.235
Ke = 0.235

a = 1
b = (Jm*Ra + La*Bm)/(La*Jm)
c = (Ke*Kt + Ra*Bm)/(La*Jm)

delta = b**2 - 4*a*c
x1 = (-b-math.sqrt(delta))/(2*a)
x2 = (-b+math.sqrt(delta))/(2*a)

U = 12
Tc = 0.05
K = (Kt*U-Tc*Ra)/(Jm*La)

B1 = K/(x1*x2)
B2 = (K-Tc*x1/Jm)/(x1*(x1-x2))
B3 = (K-Tc*x2/Jm)/(x2*(x2-x1))

t = np.linspace(0,1,1000)
wt0 = B1+B2+B3
wt = B1+ B2*np.exp(x1*t)+ B3*np.exp(x2*t) - wt0

plt.plot(t,wt, label = "Speed")
plt.legend()
plt.show()