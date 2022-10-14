
#include <math.h>
#include <stdio.h>
#include "Segment7.h"

Segment7::Segment7(float _t, float _Vm, float _Am, float _Jm){
    Jmax = _Jm;
    Amax = _Am;
    Vmax = _Vm;
    V0 = Vmax;
    index = _t;

    T = 0;t1 = 0;t3 = 0;t2 = 0;t4 = 0;t5 = 0;t6 = 0;
    a1 = Jmax;a2 = 0;a3 = -Jmax;a4 = 0;a5 = -Jmax;a6 = 0;a7 = Jmax;

    b1 = 0;b2 = 0;b3 = 0;b4 = 0;b5 = 0;b6 = 0;b7 = 0;
    c1 = 0;c2 = 0;c3 = 0;c4 = 0;c5 = 0;c6 = 0;c7 = 0;
    d1 = 0;d2 = 0;d3 = 0;d4 = 0;d5 = 0;d6 = 0;d7 = 0;

    position = 0;
    velocity = 0;
    time = 0;
    finished = true;
    Sign = 1;
}

void Segment7::get_data(float t){
    if ((0<t) and (t<= t1)){
        position = t*t*t*a1/6 + t*t*b1/2 + t*c1 +d1;
        velocity = t*t*a1/2 + t*b1 + c1;
    }
    else if ((t1<t) and (t<= t2)){
        position = t*t*t*a2/6 + t*t*b2/2 + t*c2 +d2;
        velocity = t*t*a2/2 + t*b2 + c2;
    }
    else if ((t2<t) and (t<= t3)){
        position = t*t*t*a3/6 + t*t*b3/2 + t*c3 +d3;
        velocity = t*t*a3/2 + t*b3 + c3;
    }
    else if ((t3<t) and (t<= t4)){
        position = t*t*t*a4/6 + t*t*b4/2 + t*c4 +d4;
        velocity = t*t*a4/2 + t*b4 + c4;
    }
    else if ((t4<t) and (t<= t5)){
        position = t*t*t*a5/6 + t*t*b5/2 + t*c5 +d5;
        velocity = t*t*a5/2 + t*b5 + c5;
    }
    else if ((t5<t) and (t<= t6)){
        position = t*t*t*a6/6 + t*t*b6/2 + t*c6 +d6;
        velocity = t*t*a6/2 + t*b6 + c6;
    }
    else if ((t6<t) and (t< T)){
        position = t*t*t*a7/6 + t*t*b7/2 + t*c7 +d7;
        velocity = t*t*a7/2 + t*b7 + c7;
    }

    position = 2*q0 - position;
    printf("%2.2f \r\n",position);
    // velocity = 2*v0 - velocity;
}

float Segment7::get_position(void){
	return position;
}

float Segment7::get_velocity(void){
	return velocity;
}

void Segment7::operator() (float sp){
	float delta = sp-qf;
	if ((delta != 0) && ((time > T) || (time == 0))){
        q0 = qf;
		qf = sp;
        
        T = (Amax/Jmax) + (Vmax/Amax) + (qf/Vmax);

        t1 = Amax/Jmax;
        t3 = t1 + (Vmax/Amax);
        t2 = t3 - t1;

        t4 = T - t3;
        t5 = T - t2;
        t6 = T - t1;

        b1 = 0;
        b2 = Amax;
        b3 = Amax + Jmax*t2;
        b4 = 0;
        b5 = Jmax*t4;
        b6 = -Amax;
        b7 = -Amax - Jmax*t6;

        c1 = 0;
        c2 = ((a1*t1*t1)/2 + b1*t1 + c1) - ((a2*t1*t1)/2 + b2*t1);
        c3 = ((a2*t2*t2)/2 + b2*t2 + c2) - ((a3*t2*t2)/2 + b3*t2);
        c4 = ((a3*t3*t3)/2 + b3*t3 + c3) - ((a4*t3*t3)/2 + b4*t3);
        c5 = ((a4*t4*t4)/2 + b4*t4 + c4) - ((a5*t4*t4)/2 + b5*t4);
        c6 = ((a5*t5*t5)/2 + b5*t5 + c5) - ((a6*t5*t5)/2 + b6*t5);
        c7 = ((a6*t6*t6)/2 + b6*t6 + c6) - ((a7*t6*t6)/2 + b7*t6);

        d1 = 0;
        d2 = ((a1*t1*t1*t1)/6 + (b1*t1*t1)/2 + c1*t1 + d1) - ((a2*t1*t1*t1)/6 + (b2*t1*t1)/2 + c2*t1);
        d3 = ((a2*t2*t2*t2)/6 + (b2*t2*t2)/2 + c2*t2 + d2) - ((a3*t2*t2*t2)/6 + (b3*t2*t2)/2 + c3*t2);
        d4 = ((a3*t3*t3*t3)/6 + (b3*t3*t3)/2 + c3*t3 + d3) - ((a4*t3*t3*t3)/6 + (b4*t3*t3)/2 + c4*t3);
        d5 = ((a4*t4*t4*t4)/6 + (b4*t4*t4)/2 + c4*t4 + d4) - ((a5*t4*t4*t4)/6 + (b5*t4*t4)/2 + c5*t4);
        d6 = ((a5*t5*t5*t5)/6 + (b5*t5*t5)/2 + c5*t5 + d5) - ((a6*t5*t5*t5)/6 + (b6*t5*t5)/2 + c6*t5);
        d7 = ((a6*t6*t6*t6)/6 + (b6*t6*t6)/2 + c6*t6 + d6) - ((a7*t6*t6*t6)/6 + (b7*t6*t6)/2 + c7*t6);

        time = 0;
        finished = false;
	}
    if (time <= T){
    	time += index;
    	get_data(time);
    }
    else{
    	finished = true;
    	get_data(T);
    }
}

bool Segment7::is_finished(void){
    return finished;
}


