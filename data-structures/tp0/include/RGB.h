#ifndef RGB_H
#define RGB_H

#include <iostream>

class RGB{
    public:
        uint8_t r;
        uint8_t g;
        uint8_t b;

        RGB();
        RGB(uint8_t red, uint8_t green, uint8_t blue);

        friend std::ostream& operator<< (std::ostream& os, RGB rgb);
};

#endif