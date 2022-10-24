Ra = 2;
La = 0.23;
Jm = 0.000052;
Bm = 0.01;
Kt = 0.235;
Ke = 0.235;

A = [-Ra/La -Ke/La; Kt/Jm -Bm/Jm]
B = [1/La; 0]
C = [0 1]
D = [0]

Mq = [C;C*A]
rank(Mq)

Mc = [B A*B]
rank(Mc)


