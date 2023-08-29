#ifndef SG_H
#define SG_H

// THIS SHOULD CONTAIN FUNCTIONS THAT TAKE [INSTRUMENT (LIKE IN XETRPROJ.H), TIME, FREQ, AMP] AND RETURN SINGLE SAMPLE, LIKE FUNCTIONS THAT ARE HERE NOW

#include <math.h>

namespace waveforms {
    short Sine(double time, double freq, double amp) {
        double tpc = 44100.0 / freq;
        double cycles = time / tpc;
        double rad = 6.283185307 * cycles;
        short result = 32767 * amp * sin(rad);
        return result;
    }

    short Square(double time, double freq, double amp) {
        double tpc = 44100.0 / freq;
        double cycles = time / tpc;
        double rad = 6.283185307 * cycles;
        double d = ((sin(rad) > 0) * 2) - 1;
        short result = 32767 * amp * d;
        return result;
    }
}

#endif
