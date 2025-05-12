#include "RGB.h"

RGB::RGB(){}

RGB::RGB(uint8_t red, uint8_t green, uint8_t blue){
    r = red;
    g = green;
    b = blue;
}

std::ostream& operator<< (std::ostream& os, RGB rgb){
    
    os << (unsigned)rgb.r << " ";
    os << (unsigned)rgb.g << " ";
    os << (unsigned)rgb.b << " ";

    return os;
}