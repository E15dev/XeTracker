#include "xetrproj.hpp"
#include "sg.h"
#include <math.h>
#include <cstdint>

double waveforms::getSpc(double freq) { return 44100.0/freq; } // get samples per cycle

short waveforms::WTData(double time, double freq, uint8_t data[255]) {
    return 256*static_cast<int8_t>(data[1+static_cast<int8_t>(floor(fmod(time/waveforms::getSpc(freq), 1)*126))]); // 126 because single frame in wavetable is 127 bytes
}

short waveforms::Sine(double time, double freq, double amp) {
    double rad = 6.283185307 * time/(44100.0/freq);
    short result = 32767 * amp * sin(rad);
    return result;
}

// WIP
short waveforms::fromInstrument(double time, double freq, double amp, cf::Instrument instr) {
    short out;
    if (instr.type == 0x50) { return 0; } // "P", ignoring data, return 0
    if (instr.type == 0x77) { out = WTData(time, freq, instr.data); } // "w"
    return out*amp;
}
