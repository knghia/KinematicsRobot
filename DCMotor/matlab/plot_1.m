clear;
clc;

Ra = 2;
La = 0.23;
Jm = 0.000052;
Bm = 0.01;
Kt = 0.235;
Ke = 0.235;
Tc = 0.05;
Uin = 12;

ts = [-Tc*La -Tc*Ra Kt*Uin 0];
ms = [Jm*La (Jm*Ra + Bm*La) Bm*Ra Kt*Ke 0]

sys = tf(ts,ms);
step(sys);


