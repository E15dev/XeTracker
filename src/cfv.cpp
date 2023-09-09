#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <algorithm>
#include "xetrproj.h"

void phex(uint8_t b) {
    printf("%02x ", b);
}

int main() {
    std::string path;
    getline(std::cin, path);
    std::ifstream file(path, std::ios::in | std::ios::binary);
    if (!file.is_open()) {return 1;};
    std::istream_iterator<uint8_t> start(file), end;
    file >> std::noskipws;
    std::vector<uint8_t> data(start, end);

//    for(int i = 0; i<data.size(); i++) { // just print all bytes from data as hex
//        phex(data[i]);
//    };

    uint8_t fsig[8]; std::copy_n(std::begin(data), 8, std::begin(fsig));
    uint16_t fver = ((uint16_t)data[8] << 8) | data[9];
    uint8_t ecn[2]; std::copy_n(std::next(std::begin(data), 10), 2, std::begin(ecn));
    uint8_t name[128]; std::copy_n(std::next(std::begin(data), 12), 128, std::begin(name));
    uint8_t author[64]; std::copy_n(std::next(std::begin(data), 140), 64, std::begin(author));
    uint16_t timeS = ((uint16_t)data[204] << 8) | data[205];
    int8_t rootnote = static_cast<int8_t>(data[206]);
    uint16_t tempo = ((uint16_t)data[207] << 8) | data[208];
    uint8_t insc = data[209];
    uint8_t patc = data[210];
    cf::Instrument instruments[insc]; for(int i = 0; i<insc; i++) {
        instruments[i].type = data[211+(sizeof(cf::Instrument)*i)];
        std::copy_n(std::next(std::begin(data), 211+(sizeof(cf::Instrument)*1)+1), 255, std::begin(instruments[i].data));};
    cf::Pattern patterns[patc]; for(int i = 0; i<patc; i++) {
        patterns[i].locked = data[211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*i)];
        patterns[i].muted = data[211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*i)+1];
        patterns[i].prlen = data[211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*i)+2];
        patterns[i].ofs = data[211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*i)+3];
        patterns[i].profs = static_cast<int8_t>(data[211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*i)+4]);
        patterns[i].iid = data[211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*i)+5];
        for(int j = 0; j<cf::MPL; j++) {
            patterns[i].notes[j].volume = data[211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*i)+6+(2*j)];
            patterns[i].notes[j].pitch = static_cast<int8_t>(data[211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*i)+6+(2*j)+1]);};};
    uint8_t fend[64]; std::copy_n(std::next(std::begin(data), 211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*patc)), 64, std::begin(fend));

    // replace with function for everything, inputs color, len, base(num), data
    std::cout << "\033[0;7m"; for(int i = 0; i<8; i++) { phex(data[i]);}; // fsig
    std::cout << "\033[0;7;35m"; for(int i = 0; i<2; i++) {phex(data[8+i]);}; // ver
    std::cout << "\033[0;35;47m"; for(int i = 0; i<2; i++) {phex(data[10+i]);}; // ecn
    std::cout << "\033[0;36m"; for(int i = 0; i<128; i++) {phex(data[12+i]);}; // name
    std::cout << "\033[0;34m"; for(int i = 0; i<64; i++) {phex(data[140+i]);}; // author
    std::cout << "\033[0;42m"; for(int i = 0; i<2; i++) {phex(data[204+i]);}; // time spent
    std::cout << "\033[0;41m"; phex(data[206]); // root note
    std::cout << "\033[0;43m"; for(int i = 0; i<2; i++) {phex(data[207+i]);}; // tempo
    std::cout << "\033[0;7;31m"; phex(data[209]); // insc
    std::cout << "\033[0;7;32m"; phex(data[210]); // patc
    std::cout << "\033[0;31m"; for(int i = 0; i<insc*sizeof(cf::Instrument); i++) {phex(data[211+i]);}; // instruments
    std::cout << "\033[0;32m"; for(int i = 0; i<patc*sizeof(cf::Pattern); i++) {phex(data[211+(sizeof(cf::Instrument)*insc)+i]);}; // patterns
    std::cout << "\033[0;7m"; for(int i = 0; i<64; i++) {phex(data[211+(sizeof(cf::Instrument)*insc)+(sizeof(cf::Pattern)*patc)+i]);}; // end
    std::cout << "\033[0m" << std::endl;

    std::cout << std::endl;
    if (cf::cmpsig(fsig)) {std::cout<<"valid file sig"<<std::endl;} else {std::cout<<"invalid file sig"<<std::endl;};
    std::cout << "encoded by "; for (int i = 0; i<2; i++) {std::cout << ecn[i];}; std::cout << std::endl;
    return 0;
}
