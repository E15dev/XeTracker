#include <cmath>

#ifndef P2F_H
#define P2F_H

namespace p2f {
    float bfqs[12] = {
    440.00,     // a
    466.16,     // a#
    493.88,     // b
    523.25,     // c
    554.37,     // c#
    587.33,     // d
    622.25,     // d#
    659.25,     // e
    698.46,     // f
    739.99,     // f#
    783.99,     // g
    830.61};    // g#

    float convert(int p) {
        int oct = std::floor(p / 12.0);
        int mp = (12 + (p % 12)) % 12;
        return bfqs[mp]*std::pow(2, oct);
    }
}

#endif
