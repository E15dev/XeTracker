#include "xetrproj.hpp"

#include <cstring>
#include <cstdint>

#include <iostream>
#include <iterator>
#include <vector>
#include <algorithm>

cf::Instrument cf::getInstrumentEmpty() { cf::Instrument i; i.type = 0x50; return i; } // type is P, data is ignored anyway. whatever it will be, it doesnt matter
cf::Note cf::getNoteEmpty() { cf::Note n; n.volume = 0; n.pitch = 0; return n; }
cf::Pattern cf::getPatternEmpty() { cf::Pattern p; p.locked = false; p.muted = false; p.prlen = 8; p.ofs = 0; p.profs = 0; p.iid = 0; for (int i=0; i<MPL; i++) {p.notes[i] = getNoteEmpty();} return p; }

cf::Project::Project(std::vector<uint8_t> data) {
    std::copy_n(std::begin(data), 8, std::begin(fsig));
    if (!cmpsig(fsig)) { std::cerr << "PROJECT LOADING FAILED WRONG FSIG" << std::endl; exit(-2);};
    if (!cmpver(((uint16_t)data[8] << 8) | data[9])) { std::cerr << "PROJECT FAILED, WRONG VERSION" << std::endl; exit(-3);};
    std::copy_n(std::next(std::begin(data), 10), 2, std::begin(ecn));
    std::copy_n(std::next(std::begin(data), 12), 128, std::begin(name));
    std::copy_n(std::next(std::begin(data), 140), 64, std::begin(author));
    timeS = ((uint16_t)data[204] << 8) | data[205];
    rootnote = static_cast<int8_t>(data[206]);
    tempo = ((uint16_t)data[207] << 8) | data[208];
    insc = 0; patc=0; // NEEDS TO BE 0 ON START
    instruments = nullptr; for (uint8_t i = 0; i<data[209]; i++) {
        uint8_t tmp[256]; std::copy_n(std::next(std::begin(data), 211+(sizeof(Instrument)*i)), 256, std::begin(tmp));
        Instrument tmpInstr;
        memcpy(&tmpInstr, tmp, sizeof(Instrument));
        appendInstrument(tmpInstr);
    };
    patterns = nullptr; for (uint8_t i = 0; i<data[210]; i++) {
        uint8_t tmp[134]; std::copy_n(std::next(std::begin(data), 211+(sizeof(Instrument)*insc)+(sizeof(Pattern)*i)), 134, std::begin(tmp));
        Pattern tmpPattrn;
        memcpy(&tmpPattrn, tmp, sizeof(Pattern));
        appendPattern(tmpPattrn);
    };
    std::copy_n(std::next(std::begin(data), 211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*patc)), 64, std::begin(fend));
}

void cf::Project::appendInstrument(Instrument instr) {
    insc++;
    Instrument* tmp = new Instrument[insc];
    for (uint8_t i = 0; i < insc-1; i++) { tmp[i] = instruments[i]; };
    delete[] instruments;
    instruments = tmp;
    instruments[insc-1] = instr;
}

void cf::Project::setInstrument(uint8_t i, Instrument instr) { instruments[i] = instr; }
cf::Instrument cf::Project::getInstrument(uint8_t i) { return instruments[i]; }

void cf::Project::appendPattern(Pattern patrn) {
    patc++;
    Pattern* tmp = new Pattern[patc];
    for (uint8_t i = 0; i < patc-1; i++) { tmp[i] = patterns[i]; };
    delete[] patterns;
    patterns = tmp;
    patterns[patc-1] = patrn;
}

void cf::Project::setPattern(uint8_t i, Pattern patrn) { patterns[i] = patrn; }
cf::Pattern cf::Project::getPattern(uint8_t i) { return patterns[i]; }
