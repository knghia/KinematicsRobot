
#ifndef LSPB_H
#define LSPB_H

#ifdef __cplusplus
extern "C"{
#endif
#include <inttypes.h>
#include <stdbool.h>

class LSPB{

private:
	float t0, tf;
	float q0, qf;

	float V;
	float tb = 0;

	float t;
	float index;
	float position;
	bool finished = false;
	float Vo;
	float alpha;

public:
	LSPB(float _Vo, float _t, float _alpha);
	void operator()(float _sp);
	void operator()(float _qf, float _q0);

	void get_value(float _t);
	float get_position(void);
	bool is_finished();

	void set_Vo_alpha(float v, float a);
};

#ifdef __cplusplus
}
#endif
#endif
