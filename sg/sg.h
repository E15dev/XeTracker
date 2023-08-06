#ifndef SG_H
#define SG_H

#include <math.h>

namespace sound {
    short SineWave(double time, double freq, double amp) {
        double tpc = 44100 / freq;
        double cycles = time / tpc;
        double rad = 6.283185307 * cycles;
        short amplitude = 32767 * amp;
        short result = amplitude * sin(rad);
        return result;
    }
}

#endif
