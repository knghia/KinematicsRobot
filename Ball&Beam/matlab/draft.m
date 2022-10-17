clear;
clc;


h = 0.08
h1 = 0.0
l = 0.4
d = 0.02
k = 0.08
xd = 0.4 - d

syms cosTheta sinTheta;

A = -2*(xd+d*cosTheta)*l;
B = -2*(h1+d*sinTheta - h)*l;
C = k^2 - (xd+d*cosTheta)^2 - (h1+d*sinTheta - h)^2 - l^2;
delta = B*2 + (A+C)*(A-C);

t1 = (-B+sqrt(delta))/(-A-C);
alpha = 2*atan(t1)