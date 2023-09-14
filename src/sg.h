#include "xetrproj.hpp" // i hope doing this wont break anything if i include same thing in program including this one

#ifndef SG_H
#define SG_H

#include <math.h>

namespace waveforms {
    double getCycles(double time, double freq) { return time/(44100.0/freq); } // time / times per cycle

    short _WTSine(double time, double freq) { return sin(6.283185307 * getCycles(time, freq))*32768; } // TODO DELETE AFTER IMPLEMENTING REAL WAVETABLES

    short _WTData(double time, double freq, uint8_t data[255]) {
        double tpc = 44100.0/freq;
//        printf("%f: %d\n", time, static_cast<int8_t>(data[1+static_cast<int8_t>(floor(fmod(time/tpc, 1)*127))]));
        return 256*static_cast<int8_t>(data[1+static_cast<int8_t>(floor(fmod(time/tpc, 1)*127))]);
    }

    // THIS WILL BE DELETED AFTER IMPLEMENTING fromInstrument
    short Sine(double time, double freq, double amp) {
        double rad = 6.283185307 * getCycles(time, freq);
        short result = 32767 * amp * sin(rad);
        return result;
    }

    short Square(double time, double freq, double amp) {
        double rad = 6.283185307 * getCycles(time, freq);
        double d = ((sin(rad) > 0) * 2) - 1;
        short result = 32767 * amp * d;
        return result;
    }

    // WIP of generator from instrument
    short fromInstrument(double time, double freq, double amp, cf::Instrument instr) {
        short out;
        if (instr.type == 0x50) { return 0; } // "P", ignoring data, return 0
        if (instr.type == 0x57) { if (instr.data[0] == 0x00) {out = _WTSine(time, freq); }; } // "W", only sine works for now
        if (instr.type == 0x77) { out = _WTData(time, freq, instr.data); } // "w"
        return out*amp;
    }
}

#endif
