#include <stdio.h>
#include <iostream>
#include <math.h>
#include <fstream>
#include "fuzzy.h"
using namespace std;

class GAUSSIAN{
    private:
        f32 mu,sigma;
        f32 t, g_x;
    public:
        GAUSSIAN(f32 a,f32 b);
        f32 get_time(void);
        f32 get_value(void);
        void update(void);
};

GAUSSIAN::GAUSSIAN(f32 a, f32 b){
    mu = a;
    sigma = b;
    t = -10;
}

f32 GAUSSIAN::get_time(void){
    return t;
}

f32 GAUSSIAN::get_value(void){
    return g_x;
}

void GAUSSIAN::update(void){
    f32 up;
    t+=0.01;
    up = -((t-mu)*(t-mu)/(2*sigma));
    g_x = exp(up)/sigma;
}

int main(void){
    ofstream myfile;
    myfile.open ("data.txt");

    GAUSSIAN gau = GAUSSIAN(0,5.31);
    for(i16 i=0;i<5000;i++){
        gau.update();
        myfile<<gau.get_time()<<" "<<gau.get_value()<<endl;
    }
    myfile.close();
    return 1;   
}