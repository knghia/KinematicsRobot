clear;
clc;

syms mB mb rB JB Jb g x alpha x_dot alpha_dot l d t;

L = (1/2)*(mB+JB/rB)*x_dot^2 + ...
    (1/2)*(mB*x^2+Jb)*alpha_dot^2 - ...
    g*sin(alpha)*(mB*x+mb*l/2)

L_x_dot = diff(L,x_dot)
L_x = diff(L,x)


L_alpha_dot = diff(L,alpha_dot)
L_alpha = diff(L,alpha)