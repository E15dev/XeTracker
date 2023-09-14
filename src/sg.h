#include "xetrproj.hpp" // i hope doing this wont break anything if i include same thing in program including this one

#ifndef SG_H
#define SG_H

#include <math.h>

namespace waveforms {
    short _WTData(double time, double freq, uint8_t data[255]) {
        double tpc = 44100.0/freq;
        return 256*static_cast<int8_t>(data[1+static_cast<int8_t>(floor(fmod(time/tpc, 1)*126))]); // 126 because its from 0 to 127
    }

    // WIP of generator from instrument
    short fromInstrument(double time, double freq, double amp, cf::Instrument instr) {
        short out;
        if (instr.type == 0x50) { return 0; } // "P", ignoring data, return 0
        if (instr.type == 0x77) { out = _WTData(time, freq, instr.data); } // "w"
        return out*amp;
    }
}

#endif
