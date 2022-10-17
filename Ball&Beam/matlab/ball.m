clear;
clc;

mB = 0.029;
mb = 0.334;
rB = 0.0095;
l = 0.4;
JB = (2/5)*mB*rB^2;
Jb =  (1/3)*mB*l^2;
g = 9.8;

%
h = 0.08;
h1 = 0.0;
d = 0.02;
k = 0.08;
xd = 0.4 - d;
PI = 3.14159265359;

% A = -2*(d*cos(theta)+l)*l;
% B = -2*(d*sin(theta)-h1)*l;
% C = k^2 - (d*cos(theta)+l)^2 - (d*cos(theta)-h1)^2 - l^2;
% delta = B^2 + (A+C)*(A-C);
% t1 = (-B + sqrt(delta))/(-A-C);
% alpha = arctan(t1)*2;

% dc motor
Ra = 2;
La = 0.23;
Jm = 0.000052;
Bm = 0.01;
Kt = 0.235;
Ke = 0.235;


