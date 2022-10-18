
#include <iostream>
#include <fstream>
using namespace std;
#include "LSPB.h"

int main(void){
    LSPB scuver{32, 0.01, 1.5};
    ofstream myfile;
    myfile.open ("data.txt");

    scuver.set_Vo_alpha(32,32);

    while(1){
		scuver(100,40);
		float velocity_sp = scuver.get_position();
        myfile <<velocity_sp<<"\n";
        if (scuver.is_finished()){
            break;
        }
    }
    myfile.close();

    return 1;
}