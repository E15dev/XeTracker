#include "xetrproj.hpp" // i hope doing this wont break anything if i include same thing in program including this one

#ifndef SG_H
#define SG_H

#include <math.h>

namespace waveforms {
    double getSpc(double freq) { return 44100.0/freq; } // get samples per cycle

    short WTData(double time, double freq, uint8_t data[255]) {
        return 256*static_cast<int8_t>(data[1+static_cast<int8_t>(floor(fmod(time/getSpc(freq), 1)*126))]); // 126 because single frame in wavetable is 127 bytes
    }

    // WIP of generator from instrument
    short fromInstrument(double time, double freq, double amp, cf::Instrument instr) {
        short out;
        if (instr.type == 0x50) { return 0; } // "P", ignoring data, return 0
        if (instr.type == 0x77) { out = WTData(time, freq, instr.data); } // "w"
        return out*amp;
    }
}

#endif
