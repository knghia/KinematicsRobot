
#include <iostream>
#include <fstream>
using namespace std;
#include "LSPB.h"

int main(void){
    LSPB scuver{150, 0.01};
    ofstream myfile;
    myfile.open ("data.txt");

    while(1){
		scuver(100);
		float velocity_sp = scuver.get_velocity();
        myfile <<velocity_sp<<"\n";
        if (scuver.is_finish()){
            break;
        }

    }
    myfile.close();

    return 1;
}