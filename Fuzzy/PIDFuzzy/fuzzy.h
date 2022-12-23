#ifndef FUZZY_H
#define FUZZY_H

#include<inttypes.h>
#define u08 uint8_t
#define u16 uint16_t
#define u32 uint32_t

#define i08 int8_t
#define i16 int16_t
#define i32 int32_t

#define f32 float

#ifdef __cplusplus
extern "C" {
#endif

#define _constrain(amt,low,high) ((amt)<(low)?(low):((amt)>(high)?(high):(amt)))

#define NB  -40
#define NM  -26
#define NS  -6
#define ZZ  0
#define PS  6
#define PM  26
#define PB  40

extern void fuzzy_init(void);
extern i08 fuzzy_get_nuy(f32 input, f32 *nuy);
extern f32 fuzzy_get_value(f32 e, f32 ce);


typedef struct{
	f32 K, Kp, Ki, Kd;
	f32 Limit;
	f32 uLimit;
	f32 dLimit;
	f32 P, I, D;
	f32 PartError;
	f32 Output;
	f32 FV;
}PIDFuzzy;

extern f32 pid_fuzzy_upload(PIDFuzzy* pid,f32 e);

#ifdef __cplusplus
}
#endif

#endif
