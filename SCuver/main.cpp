#include <iostream>
#include <inttypes.h>
#include <math.h>
using namespace std;
#define u08 uint8_t
#define u16 uint16_t
#define f32 float

class SecondOrderDynamics{
private:
    f32 xp;
    f32 y, yd;
    f32 k1, k2, k3;
    const f32 T = 0.01;
public:
    SecondOrderDynamics(f32 f,f32 z,f32 r);
    void Update(f32 x);
};

SecondOrderDynamics::SecondOrderDynamics(f32 f,f32 z,f32 r){
    k1 = z/(M_PI*f);
    k2 = 1/((2*M_PI*f)*(2*M_PI*f));
    k2 = r*z/(2*M_PI*f);
    xp = 0;
    y = 0;
    yd = 0;
} 

SecondOrderDynamics::Update(float x){
    float xd = (x-xp)/T;
    xp = x;
    y = y + T*yd;
    yd = yd + T*(x+k3*xd - y - k1*yd)/k2;
    return y;
}

int main(void){
    SecondOrderDynamics scuver = SecondOrderDynamics(0, 1, 0);
    

}