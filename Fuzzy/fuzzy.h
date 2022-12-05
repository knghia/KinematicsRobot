#ifndef FUZZY_H
#define FUZZY_H

#ifdef __cplusplus
extern "C" {
#endif

#include<inttypes.h>
#define u08 uint8_t
#define u16 uint16_t
#define u32 uint32_t

#define i08 int8_t
#define i16 int16_t
#define i32 int32_t
#define f32 float

#define NB  -30
#define NM  -20
#define NS  -10
#define ZZ  0
#define PS  10
#define PM  20
#define PB  30
#define _constrain(amt,low,high) ((amt)<(low)?(low):((amt)>(high)?(high):(amt)))

extern void fuzzy_init(void);
extern i08 fuzzy_get_nuy(f32 input, f32 *nuy);
extern f32 fuzzy_get_value(f32 e, f32 ce);

typedef struct{
	f32 K, Kp, Ki, Kd;
	f32 Limit;
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
