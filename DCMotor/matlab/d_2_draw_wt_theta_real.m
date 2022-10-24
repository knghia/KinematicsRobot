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

Uin = 24;

% % % % % % % % % % %
K = Uin*Kt/(La*Jm);
A1 = 1/(x1*x2);
A2 = 1/(x1*(x1-x2));
A3 = 1/(x2*(x2-x1));
t = linspace(0, 2.5, 2000);

wt = K*(A2*exp(x1*t) + A3*exp(x2*t) - (A2+A3));
thetat = K*((A2/x1)*exp(x1*t) + (A3/x2)*exp(x2*t) - (A2+A3)*t - (A2/x1 + A3/x2));

subplot(2,1,1);
plot(t,wt)
title('Step Response Wt');
subplot(2,1,2); 
plot(t,thetat)
title('Step Response Theta');


