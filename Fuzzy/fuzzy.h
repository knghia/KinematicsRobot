#ifndef FUZZY_H
#define FUZZY_H

#ifdef __cplusplus
extern "C" {
#endif

#define NB  -3
#define NM  -2
#define NS  -1
#define ZZ  0
#define PS  1
#define PM  2
#define PB  3

#define DE_NB    -24
#define DE_NM    -16
#define DE_NS    -8
#define DE_ZZ    0
#define DE_PS    8
#define DE_PM    16
#define DE_PB    24

#define u08 uint8_t
#define u16 uint16_t
#define u32 uint32_t
#define f32 float

extern void fuzzy_init(void);
void fuzzy_get_nuy(f32 tau);

#ifdef __cplusplus
}
#endif

#endif
