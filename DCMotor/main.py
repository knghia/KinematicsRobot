
import math 
from math import e
import numpy as np
import matplotlib.pyplot as plt

Ra = 2.32
La = 0.238*10e-3
Jm = 10.8*10e-7
Bm = 0.0
Kt = 2.85*10e-3
Ke = 1/(408*0.10472)

# print(Ra, La, Jm, Bm, Kt, Ke)

_A = La*Jm/Kt
_B = (Jm*Ra + La*Bm)/Kt
_C = (Ke*Kt + Ra*Bm)/Kt

Delta = _B**2 - 4*_A*_C

alpha = (-_B + math.sqrt(Delta))/(2*_A)
beta = (-_B - math.sqrt(Delta))/(2*_A)

Uin = 12

_C1 = -alpha*((Uin/_C)/(alpha - beta))
_C2 = beta*((Uin/_C)/(alpha - beta))

t = np.linspace(0,1,5000)

omega = _C1*e**(alpha*t)+ _C2*e**(beta*t) + (Uin/_C)
theta = (_C1/alpha)*e**(alpha*t)+ (_C2/beta)*e**(beta*t) + (Uin/_C)*t + Omeha

plt.plot(t,omega)
plt.plot(t,theta)
plt.show()