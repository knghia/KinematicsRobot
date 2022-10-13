
from cProfile import label
import numpy as np
import math
import matplotlib.pyplot as plt

g = 9.8
mu = 0.2
alpha = np.pi/6
rb = 0.02
mb = 0.2
L = 2

a = 1
b = mu*g*np.cos(alpha)
c = 0

delta = b**2 - 4*a*c

x2 = (-b-np.sqrt(delta))/(2*a)
x1 = (-b+np.sqrt(delta))/(2*a)

C1 = np.tan(alpha)/(x2*mu)
C2 = -np.tan(alpha)/(x2*mu)

t = np.linspace(0,10,2000)
xt = C1 + C2*np.exp(x2*t) + t*np.tan(alpha)/mu
vt = x2*C2*np.exp(x2*t) + np.tan(alpha)/mu
at = x2*x2*C2*np.exp(x2*t)

plt.plot(t,xt,label="xt")
plt.plot(t,vt,label="vt")
plt.plot(t,at,label="at")
plt.legend()
plt.show()
