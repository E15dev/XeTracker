#ifndef XETRPROJ_H
#define XETRPROJ_H

namespace cf {
    uint8_t MPL = 64;
    uint16_t CURRENT_VERSION = 5;
    uint8_t ECN[2] = {0x63, 0x2b};

    uint8_t SIG[8] = {0x58, 0x65, 0x54, 0x72, 0x50, 0x72, 0x6f, 0x6a}; // "XeTrProj"
    uint8_t END[64] = { 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33, 0x3a, 0x33,
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

    # pragma pack(1)
    struct Note {
        uint8_t volume;
        int8_t pitch;
    };  // 2

    # pragma pack(1)
    struct Pattern {
        bool locked;    // i hope its 1 byte
        bool muted;
        uint8_t prlen;
        uint8_t ofs;
        int8_t profs;
        uint8_t iid;    // instrument id
        Note notes[64];
    };  // 134

    bool cmpsig(uint8_t csig[8]) {
        for(int i = 0; i<8; i++) {
            if (csig[i] != SIG[i]) {return false;};
        };
        return true;
    };

    Note getNoteEmpty() { Note n; n.volume = 0; n.pitch = 0; return n; }
    Pattern getPatternEmpty() { Pattern p; p.locked = false; p.muted = false; p.prlen = 8; p.ofs = 0; p.profs = 0; p.iid = 0; for (int i=0; i<MPL; i++) {p.notes[i] = getNoteEmpty();} return p; }
    Instrument getInstrumentEmpty() { Instrument i; i.type = 0x50;  return i; } // type is P, data is ignored anyway. whatever it will be, it doesnt matter
}

#endif
