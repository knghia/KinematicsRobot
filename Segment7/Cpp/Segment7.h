
#ifndef Segment7_H
#define Segment7_H

#ifdef __cplusplus
extern "C"{
#endif
#include <inttypes.h>
#include <stdbool.h>

class Segment7{

private:
    float Jmax;
    float Amax;
    float Vmax;
	float V0;
    float qf;
	float q0 = 0;
    float index;

    float T,t1,t3,t2,t4,t5,t6;
	float a1,a2,a3,a4,a5,a6,a7;

    float b1,b2,b3,b4,b5,b6,b7;
	float c1,c2,c3,c4,c5,c6,c7;
	float d1,d2,d3,d4,d5,d6,d7;

	float position;
	float velocity;
	float time;
	bool finished = false;
	int8_t Sign = 1;

public:
	Segment7(float _t, float _Vm, float _Am, float _Jm);
	void operator()(float sp);
	void get_data(float _t);

	float get_position(void);
	float get_velocity(void);
	bool is_finished(void);
};

#ifdef __cplusplus
}
#endif
#endif

