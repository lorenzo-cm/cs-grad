#ifndef RANDOMIZE_H
#define RANDOMIZE_H

#include <stdlib.h>
#include "register.h"

void randomize(Register *V, int n, unsigned seed){

    srand(seed);

    for(int i = 0; i<n; i++){
        V[i].key = rand();
    }
}

#endif