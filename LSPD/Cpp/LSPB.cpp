
#include "LSPB.h"
#include <math.h>
#include <stdio.h>

LSPB::LSPB(float _Vo, float _t)
{
	t0 = 0;
	tf = 0;
	Vo = _Vo;
	V = _Vo;

	q0 = 0;
	qf = 0;

    tb = 0;

	index= _t;
	finished = false;
	position = 0;
	velocity = 0;

	t = 0;
}

float LSPB::get_position(void){
	return position;
}
float LSPB::get_velocity(void){
	return velocity;
}

void LSPB::get_value(float _t){
	if ((0<= _t) and (_t <= tb)){
    	position = q0 + _t*_t*V/(2*tb);
    	velocity = _t*V/(tb);
	}
    else if ((tb < _t) and (_t <= (tf - tb))){
        position = (V*_t + (qf + q0 - V*tf)/2);
        velocity = V;
    }
    else if (((tf - tb) < _t) and (_t < tf)){
    	position = qf- tf*tf*V/(2*tb)+ _t*V*tf/tb- _t*_t*V/(2*tb);
    	velocity = V*tf/tb- _t*V/(tb);
    }
}

void LSPB::operator() (int16_t sp){
	int16_t delta = sp-qf;
	if ((delta != 0) && ((t > tf) || (t == 0))){
		q0 = qf;
		qf = sp;

        if ((qf - q0) >= 0)
            V = Vo;
        else
            V = -Vo;

		tf = 1.5*(qf - q0)/(float)V;
        tb = (q0 - qf + V*tf)/(float)V;

        t = 0;
        finished = false;
	}
    if (t <= tf){
    	t += index;
    	get_value(t);
    }
    else{
    	finished = true;
    	get_value(tf);
    }
}

bool LSPB::is_finish(){
	return finished;
}


