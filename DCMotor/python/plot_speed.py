
import math
import numpy as np
import matplotlib.pyplot as plt

def u_t(t,t0):
    return np.array([0 if i<t0 else 1 for i in t])

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

K = Kt/(La*Jm)
A1 = 1/(x1*x2)
A2 = 1/(x1*(x1-x2))
A3 = 1/(x2*(x2-x1))
U1 = 1
U2 = 10
t1 = 1

t = np.linspace(0,2,2000)
wt0 = K*(U1*(A1+ A2 + A3) - (U1-U2)*(A2*np.exp(x1*(-t1)) + A3*np.exp(x2*(-t1))))
print(wt0)
wt = K*(U1*(A1*u_t(t,0) + A2*np.exp(x1*t) + A3*np.exp(x2*t)) - (U1-U2)*(A1*u_t(t,t1) + A2*np.exp(x1*(t-t1)) + A3*np.exp(x2*(t-t1))))-wt0
print(wt[0])


plt.plot(t,wt, label = "Speed")
plt.legend()
plt.show()