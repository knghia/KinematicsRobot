
#include "LSPB.h"
#include <math.h>
#include <stdio.h>

LSPB::LSPB(float _Vo, float _t, float _alpha){
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
	t = 0;
	alpha = _alpha;
}

float LSPB::get_position(void){
	return position;
}

void LSPB::get_value(float _t){
	if ((0<= _t) and (_t <= tb)){
    	position = q0 + _t*_t*V/(2*tb);
	}
    else if ((tb < _t) and (_t <= (tf - tb))){
        position = (V*_t + (qf + q0 - V*tf)/2);
    }
    else if (((tf - tb) < _t) and (_t < tf)){
    	position = qf- tf*tf*V/(2*tb)+ _t*V*tf/tb- _t*_t*V/(2*tb);
    }
    else{
    	position = qf;
    }
}

void LSPB::operator() (float _sp){
	float delta = _sp-qf;
	if ((delta != 0) && ((t > tf) || (t == 0))){
		q0 = qf;
		qf = _sp;

        if ((qf - q0) >= 0){
            V = Vo;
        }
        else{
            V = -Vo;
        }
        tf = alpha*(qf - q0)/V;
        tb = (q0 - qf + V*tf)/V;

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

void LSPB::operator() (float _qf, float _q0){
	float delta = _qf-qf;
	if ((delta != 0) && ((t > tf) || (t == 0))){
		q0 = _q0;
		qf = _qf;

        if ((qf - q0) >= 0){
            V = Vo;
        }
        else{
            V = -Vo;
        }
        tf = alpha*(qf - q0)/V;
        tb = (q0 - qf + V*tf)/V;

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

bool LSPB::is_finished(){
	return finished;
}

void LSPB::set_Vo_alpha(float v, float a){
	this->Vo = v;
	// if (a>2){
	// 	a = 2;
	// }
	// if (a<1){
	// 	a = 1;
	// }
	this->alpha = a;
}
