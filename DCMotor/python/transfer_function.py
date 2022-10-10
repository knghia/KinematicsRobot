import math
from xml.etree.ElementTree import C14NWriterTarget
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

K = Kt/(La*Jm)
A1 = 1/(x1*x2)
A2 = 1/(x1*(x1-x2))
A3 = 1/(x2*(x2-x1))

t = np.linspace(0,1,1000)
wt = K*(A1+ A2*np.exp(x1*t) + A3*np.exp(x2*t))
thetat = K*(A1*t+ (A2/x1)*np.exp(x1*t) + (A3/x2)*np.exp(x2*t))

plt.plot(t,wt)
plt.plot(t,thetat)
plt.show()