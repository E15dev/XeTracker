#ifndef XETRPROJ_H
#define XETRPROJ_H

#include <cstring>
#include <cstdint>

#include <iostream>
#include <vector>
#include <algorithm>

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
    Instrument getInstrumentEmpty();

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

            Project(std::vector<uint8_t>);

            void appendInstrument(Instrument);
            // TODO: REMOVE INSTRUMENTS, (LIKE FROM MIDDLE OF THING, WILL ALSO NEED TO REMAP IN ALL PATTERNS)
            void setInstrument(uint8_t i, Instrument instr);
            Instrument getInstrument(uint8_t i);
            void appendPattern(Pattern);
            // TODO: REMOVE PATTERN, should need no remaping, just copy everything except one
            void setPattern(uint8_t, Pattern);
            Pattern getPattern(uint8_t);

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
