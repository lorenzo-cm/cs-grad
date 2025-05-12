#ifndef PPMHANDLER_H
#define PPMHANDLER_H

#include "../include/Matrix.h"

void readPPM(Matrix& matrix, std::string filename);

void writePGM(Matrix& matrix, std::string filename);

void turnBW(Matrix& matrix, std::ofstream& file);

#endif