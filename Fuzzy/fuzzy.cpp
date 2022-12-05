#include "fuzzy.h"
#include <inttypes.h>
#include <stdio.h>

typedef struct{
    f32 x;
    f32 y;
}Point __attribute__((aligned (4)));

typedef struct{
    f32 a;
    f32 b;
    f32 c;
}Line __attribute__((aligned (4)));


/*
A = (xA, yA)
B = (xB, yB)

AB : (x- xA)/(xB- xA) = (y- yB)/(yB- yA)
*/

extern bool point_cvt_line(Point p1, Point p2, Line *l0){
    if (p1.x == p2.x && p1.y == p2.y){
        return false;
    }
    if (p1.x == p2.x){
        l0->a = 1; l0->b = 0; l0->c = p1.x;
        return true;
    }
    if (p1.y == p2.y){
        l0->a = 0; l0->b = 1; l0->c = p1.y;
        return true;
    }
    f32 s_a = 1/(p2.x - p1.x);
    f32 s_b = 1/(p2.y - p1.y);

    l0->a = s_a;
    l0->b = -s_b;
    l0->c = -(p1.x*s_a - p1.y*s_b);
    return true;
}

extern f32 line_get_value(Line l0, float x){
    f32 y = 0;
    y = (-l0.a*x - l0.c)/l0.b;
    return y;
}

void printLine(Line *l0,int len){
    for(int i=0;i<len;i++){
        printf("%f %f %f \r\n", l0[i].a, l0[i].b, l0[i].c);
    }
}

Line line_NB[3] = {0};
Line line_NM[4] = {0};
Line line_NS[4] = {0};
Line line_ZZ[4] = {0};
Line line_PS[4] = {0};
Line line_PM[4] = {0};
Line line_PB[3] = {0};

extern void fuzzy_init(void){
    #if !defined(NB) || !defined(NM) || !defined(NS) || !defined(ZZ) || !defined(PS) || !defined(PM) || !defined(PB)
    #error "don't define base paramters"
    #endif
    /*
        load line NB
        line NB 0: y = 1;
        line NB 1: A(NB, 1), B(NM, 0)
        line NB 2: y = 0;
    */
    Point pA, pB;
    line_NB[0].a = 0;
    line_NB[0].b = 1;
    line_NB[0].c = -1;
    pA.x = NB;pA.y = 1;
    pB.x = NM;pB.y = 0;
    point_cvt_line(pA, pB, (Line*)&line_NB[1]);
    line_NB[2].a = 0;
    line_NB[2].b = 1;
    line_NB[2].c = 0;
    /*
        load line NM
        line NM 0: y = 0;
        line NM 1: A(NB, 0), B(NM, 1)
        line NM 2: A(NM, 1), B(NS, 0)
        line NM 3: y = 0;
    */
    line_NM[0].a = 0;
    line_NM[0].b = 1;
    line_NM[0].c = 0;
    pA.x = NB;pA.y = 0;
    pB.x = NM;pB.y = 1;
    point_cvt_line(pA, pB, (Line*)&line_NM[1]);
    pA.x = NM;pA.y = 1;
    pB.x = NS;pB.y = 0;
    point_cvt_line(pA, pB, (Line*)&line_NM[2]);
    line_NM[3].a = 0;
    line_NM[3].b = 1;
    line_NM[3].c = 0;
    /*
        load line NS
        line NS 0: y = 0;
        line NS 1: A(NM, 0), B(NS, 1)
        line NS 2: A(NS, 1), B(ZZ, 0)
        line NS 3: y = 0;
    */
    line_NS[0].a = 0;
    line_NS[0].b = 1;
    line_NS[0].c = 0;
    pA.x = NM;pA.y = 0;
    pB.x = NS;pB.y = 1;
    point_cvt_line(pA, pB, (Line*)&line_NS[1]);
    pA.x = NS;pA.y = 1;
    pB.x = ZZ;pB.y = 0;
    point_cvt_line(pA, pB, (Line*)&line_NS[2]);
    line_NS[3].a = 0;
    line_NS[3].b = 1;
    line_NS[3].c = 0;
    /*
        load line ZZ
        line ZZ 0: y = 0;
        line ZZ 1: A(NS, 0), B(ZZ, 1)
        line ZZ 2: A(ZZ, 1), B(NS, 0)
        line ZZ 3: y = 0;
    */
    line_ZZ[0].a = 0;
    line_ZZ[0].b = 1;
    line_ZZ[0].c = 0;
    pA.x = NS;pA.y = 0;
    pB.x = ZZ;pB.y = 1;
    point_cvt_line(pA, pB, (Line*)&line_ZZ[1]);
    pA.x = ZZ;pA.y = 1;
    pB.x = PS;pB.y = 0;
    point_cvt_line(pA, pB, (Line*)&line_ZZ[2]);
    line_ZZ[3].a = 0;
    line_ZZ[3].b = 1;
    line_ZZ[3].c = 0;
    /*
        load line PS
        line PS 0: y = 0;
        line PS 1: A(ZZ, 0), B(PS, 1)
        line PS 2: A(PS, 1), B(PM, 0)
        line PS 3: y = 0;
    */
    line_PS[0].a = 0;
    line_PS[0].b = 1;
    line_PS[0].c = 0;
    pA.x = ZZ;pA.y = 0;
    pB.x = PS;pB.y = 1;
    point_cvt_line(pA, pB, (Line*)&line_PS[1]);
    pA.x = PS;pA.y = 1;
    pB.x = PM;pB.y = 0;
    point_cvt_line(pA, pB, (Line*)&line_PS[2]);
    line_PS[3].a = 0;
    line_PS[3].b = 1;
    line_PS[3].c = 0;
    /*
        load line PM
        line PS 0: y = 0;
        line PS 1: A(PS, 0), B(PM, 1)
        line PS 2: A(PM, 1), B(PS, 0)
        line PS 3: y = 0;
    */
    line_PM[0].a = 0;
    line_PM[0].b = 1;
    line_PM[0].c = 0;
    pA.x = PS;pA.y = 0;
    pB.x = PM;pB.y = 1;
    point_cvt_line(pA, pB, (Line*)&line_PM[1]);
    pA.x = PM;pA.y = 1;
    pB.x = PB;pB.y = 0;
    point_cvt_line(pA, pB, (Line*)&line_PM[2]);
    line_PM[3].a = 0;
    line_PM[3].b = 1;
    line_PM[3].c = 0;
    /*
        load line PB
        line PS 0: y = 0;
        line PS 1: A(PM, 0), B(PB, 1)
        line PS 2: y = 1;
    */
    line_PB[0].a = 0;
    line_PB[0].b = 1;
    line_PB[0].c = 0;
    pA.x = PM;pA.y = 0;
    pB.x = PB;pB.y = 1;
    point_cvt_line(pA, pB, (Line*)&line_PB[1]);
    line_PB[2].a = 0;
    line_PB[2].b = 1;
    line_PB[2].c = -1;
}

const int scaler[7] = {-24, -16, -8, 0, 8, 16, 24};

void fuzzy_get_nuy(f32 tau){
    f32 nuy[7] = {0};
    
    if (tau<=NB){
        nuy[0] = line_get_value(line_NB[1], tau);
    }
    else if(NB<=tau && tau<NM){
        nuy[0] = line_get_value(line_NB[2], tau);
        nuy[1] = line_get_value(line_NM[1], tau);
    }
    else if(NM<=tau && tau<NS){
        nuy[1] = line_get_value(line_NM[2], tau);
        nuy[2] = line_get_value(line_NS[1], tau);
    }
    else if(NS<=tau && tau<ZZ){
        nuy[2] = line_get_value(line_NS[2], tau);
        nuy[3] = line_get_value(line_ZZ[1], tau);
    }
    else if(ZZ<=tau && tau<PS){
        nuy[3] = line_get_value(line_ZZ[2], tau);
        nuy[4] = line_get_value(line_PS[1], tau);
    }
    else if(PS<=tau && tau<PM){
        nuy[4] = line_get_value(line_PS[2], tau);
        nuy[5] = line_get_value(line_PM[1], tau);
    }
    else if(PM<=tau && tau<PB){
        nuy[5] = line_get_value(line_PM[2], tau);
        nuy[6] = line_get_value(line_PB[1], tau);
    }
    else{
        nuy[7] = 1;
    } 
 
    printf("\r\n nuy : ");
    for(u08 i=0;i<7;i++){
        printf("%2.3f ", nuy[i]);
    }
}