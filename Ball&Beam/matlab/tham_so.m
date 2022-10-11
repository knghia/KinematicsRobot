clear;
clc;

% Ball and Beam
mB = 0.029; % mass of the ball
rB = 0.0095 % radius of the ball
JB = (2/5)*mB*rB^2;

mb = 0.334; % mass of the beam
Lb = 0.4; % beam length
Jb = (1/3)*mb*Lb^2;
g = 9.8;

% DC Motor

Ra = 2;
La = 0.23;
Jm = 0.000052;
Bm = 0.01;
Kt = 0.235;
Ke = 0.235;

