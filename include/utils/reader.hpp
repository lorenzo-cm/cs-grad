#ifndef READER_H
#define READER_H

#include <iostream>
#include <fstream>

namespace Reader{
    inline int valuesN[15];
    inline int size;

    void readN(char* filename);
    void printN();
}

#endif