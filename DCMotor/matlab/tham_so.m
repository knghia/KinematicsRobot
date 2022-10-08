Ra = 2;
La = 0.23;
Jm = 0.000052;
Bm = 0.01;
Kt = 0.235;
Ke = 0.235;

a = 1
b = (Jm*Ra + La*Bm)/(La*Jm)
c = (Ke*Kt + Ra*Bm)/(La*Jm)

delta = b^2 - 4*a*c
x1 = (-b+sqrt(delta))/(2*a)
x2 = (-b-sqrt(delta))/(2*a)

s = tf('s');
H_speed = (Kt/(La*Jm))/(s^2 + s*(Jm*Ra + La*Bm)/(La*Jm) + (Ke*Kt + Ra*Bm)/(La*Jm))
H_theta = (Kt/(La*Jm))/(s^3 + s^2*(Jm*Ra + La*Bm)/(La*Jm) + s*(Ke*Kt + Ra*Bm)/(La*Jm))

sys_tf = [H_speed ; H_theta];
inputs = {'u'};
outputs = {'speed'; 'theta'};
set(sys_tf,'InputName',inputs)
set(sys_tf,'OutputName',outputs)

step(sys_tf);




