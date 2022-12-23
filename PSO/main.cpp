#include <iostream>
#include "fuzzy.h"
using namespace std;

int main(void){
    f32 current_q_sp;
    PIDFuzzy PID_velocity = {
        .K = 0.5,
        .Kp = 0.1,
        .Ki = 0.1,
        .Kd = 0.1,
        .Limit = 24,
        .uLimit = 24,
        .dLimit = 24,
        .P = 0,.I = 0,.D = 0,
        .PartError = 0,
        .Output = 0
    };

    current_q_sp = pid_fuzzy_upload(&PID_velocity, 10);
    cout<<"current "<<current_q_sp<<endl;

    return 1;
}