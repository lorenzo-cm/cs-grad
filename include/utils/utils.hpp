#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include "register.h"

void printArray(Register *V, int n){
    if(n <= 10){
        for(int i = 0; i<n; i++){
            printf("%d ", V[i].key);
        }
        putchar('\n');
    } else printf("Array too large\n");
}

bool isSorted(Register *V, int n){
    for(int i = 0; i<n-1; i++){
        if(V[i].key > V[i+1].key) return false;
    }
    return true;
}

#endif