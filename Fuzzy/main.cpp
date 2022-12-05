#include <iostream>
#include "fuzzy.h"
using namespace std;

PIDFuzzy PID_q = {
.K = 2,
.Kp = 0.10,.Ki = 0.1,.Kd = 0.1,
.Limit = 24,
.P = 0,.I = 0,.D = 0,
.PartError = 0,
.Output = 0
};

int main(int argc, char **argv){  
    f32 v_q;
    fuzzy_init();

    v_q = pid_fuzzy_upload(&PID_q, -10);

    printf("%04f ",v_q);
    return 0;  
 }  