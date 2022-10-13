
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
	int16_t q0, qf;

	float V,Vo;
	float tb = 0;

	float t;
	float index;
	float position;
	float velocity;
	bool finished = false;

public:
	LSPB(float _V, float _t);
	void operator()(int16_t sp);
	void get_value(float _t);
	float get_position(void);
	float get_velocity(void);
	bool is_finish();
};

#ifdef __cplusplus
}
#endif
#endif

