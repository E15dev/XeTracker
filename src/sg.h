#ifndef SG_H
#define SG_H

#include "xetrproj.hpp"
#include <math.h>

namespace waveforms {
    double getSpc(double);

    short WTData(double, double, uint8_t[255]);

    short Sine(double, double, double);
    short fromInstrument(double, double, double, cf::Instrument);
}

#endif
