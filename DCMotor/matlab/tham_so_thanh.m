clear;
clc;
Ra = 2;
La = 0.23;
Jmdc = 0.000052;
Bm = 0.01;
Kt = 0.235;
Ke = 0.235;

Jm = Jmdc+ (1/2)*1*(0.01)^2;

a = 1
b = (Jm*Ra + La*Bm)/(La*Jm)
c = (Ke*Kt + Ra*Bm)/(La*Jm)

delta = b^2 - 4*a*c
x1 = (-b+sqrt(delta))/(2*a)
x2 = (-b-sqrt(delta))/(2*a)
