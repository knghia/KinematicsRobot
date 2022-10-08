
clc;

syms Jb JB R L mB mb d x x_dot alpha alpha_dot g

T = (1/2)*mB*x_dot^2 + ...
    (1/2)*(JB/R)*x_dot^2 + ...
    (1/2)*(JB+mB*x^2)*alpha_dot^2 + ...
    (1/2)*(Jb)*alpha_dot^2;

P = mB*g*x*sin(alpha)+ ...
    mb*g*(L/2)*sin(alpha);

L = T-P;

L_diff_x_dot = diff(L, x_dot)
L_diff_x = diff(L, x)

L_diff_alpha_dot = diff(L, alpha_dot)
L_diff_alpha = diff(L, alpha)


