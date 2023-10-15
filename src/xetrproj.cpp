#include "xetrproj.hpp"

#include <cstring>
#include <cstdint>

#include <iostream>
#include <fstream>
#include <sstream>
#include <iterator>
#include <vector>
#include <algorithm>
#include <chrono>

cf::Instrument cf::getInstrumentEmpty() { cf::Instrument i; i.type = 0x50; return i; } // type is P, data is ignored anyway. whatever it will be, it doesnt matter
cf::Note cf::getNoteEmpty() { cf::Note n; n.volume = 0; n.pitch = 0; return n; }
cf::Pattern cf::getPatternEmpty() { cf::Pattern p; p.locked = false; p.muted = false; p.prlen = 8; p.ofs = 0; p.profs = 0; p.iid = 0; for (int i=0; i<MPL; i++) {p.notes[i] = getNoteEmpty();} return p; }
