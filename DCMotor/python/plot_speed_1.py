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
T = 0.05
K = -Kt*Kt/(La*La*T*Jm)
Q = U*Kt/(La*T)-Ra/La
B1 = Q/((Q-x1)*(Q-x2))
B2 = x1/((x1-x2)*(x1-Q))
B3 = x2/((x2-x1)*(x2-Q))

t = np.linspace(0,2,2000)
wt0 = K*(B1+B2+B3)
wt = K*(B1*np.exp(Q*t)+ B2*np.exp(-Q*t)+ B3*np.exp(x1*t)) - wt0

plt.plot(t,wt, label = "Speed")
plt.legend()
plt.show()