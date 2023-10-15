#ifndef XETRPROJ_H
#define XETRPROJ_H

#include <cstring>
#include <cstdint>

#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

namespace cf {
    const uint8_t MPL = 64;
    const uint16_t CURRENT_VERSION = 5;
    const uint8_t ECN[2] = {0x63, 0x2b}; // "C+"

    const uint8_t SIG[8] = {0x58, 0x65, 0x54, 0x72, 0x50, 0x72, 0x6f, 0x6a}; // "XeTrProj"
    const uint8_t END[64] = { 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33,
                        0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33,
                        0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33,
                        0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33,
                        0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33,
                        0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33,
                        0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33,
                        0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33}; // a lot of ":3" according to documentation

    # pragma pack(1)
    struct Instrument {
        uint8_t type;
        uint8_t data[255];
    };  // 256
    Instrument getInstrumentEmpty(); // type is P, data is ignored anyway. whatever it will be, it doesnt matter

    # pragma pack(1)
    struct Note {
        uint8_t volume;
        int8_t pitch;
    };  // 2
    Note getNoteEmpty();

    # pragma pack(1)
    struct Pattern {
        bool locked;    // i hope its 1 byte
        bool muted;
        uint8_t prlen;
        uint8_t profs;
        int8_t ofs;
        uint8_t iid;    // instrument id
        Note notes[64];
    };  // 134
    Pattern getPatternEmpty();


    class Project {
        public:
            uint8_t name[128];
            uint8_t author[64];
            uint16_t timeS;
            int8_t rootnote;
            uint16_t tempo;
            Project(std::vector<uint8_t> data) {
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

            void appendInstrument(Instrument instr) {
                insc++;
                Instrument* tmp = new Instrument[insc];
                for (uint8_t i = 0; i < insc-1; i++) { tmp[i] = instruments[i]; };
                delete[] instruments;
                instruments = tmp;
                instruments[insc-1] = instr;
            }
            // TODO: REMOVE INSTRUMENTS, (LIKE FROM MIDDLE OF THING, WILL ALSO NEED TO REMAP IN ALL PATTERNS)
            void setInstrument(uint8_t i, Instrument instr) { instruments[i] = instr; }
            Instrument getInstrument(uint8_t i) { return instruments[i]; }

            void appendPattern(Pattern patrn) {
                patc++;
                Pattern* tmp = new Pattern[patc];
                for (uint8_t i = 0; i < patc-1; i++) { tmp[i] = patterns[i]; };
                delete[] patterns;
                patterns = tmp;
                patterns[patc-1] = patrn;
            }
            // TODO: REMOVE PATTERN, should need no remaping, just copy everything except one
            void setPattern(uint8_t i, Pattern patrn) { patterns[i] = patrn; }
            Pattern getPattern(uint8_t i) { return patterns[i]; }

        Note playerRead(uint8_t pi, int i) {
            Pattern cp = getPattern(pi);
            Note tmp = cp.notes[(cp.profs + ((i+cp.ofs)%cp.prlen)) % MPL];
            Note n;
            n.volume = tmp.volume;
            n.pitch = rootnote + tmp.pitch;
            return n;
        }

        uint8_t getPatternCount() {return patc;} // idk

        private:
            uint8_t fsig[8];
            uint16_t fver;
            uint8_t ecn[2];
            uint8_t insc;
            uint8_t patc;
            Instrument* instruments;
            Pattern* patterns;
            uint8_t fend[64];

            bool cmpsig(uint8_t csig[8]) {
                for(int i = 0; i<8; i++) { if (csig[i] != SIG[i]) {return false;}; };
                return true;
            };

            bool cmpver(uint16_t ver) {
                if (ver < CURRENT_VERSION) { std::cerr << "TOO OLD" << std::endl; return false; };
                if (ver > CURRENT_VERSION) { std::cerr << "TOO NEW" << std::endl; return false; };
                return true;
            }

        };
}

#endif
