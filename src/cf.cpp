#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <algorithm>
#include <iomanip>
#include "xetrproj.h"

using namespace std;

void phex(uint8_t b) {
    printf("%02x ", b);
}

int main()
{
    string path;
    getline(cin, path);
    ifstream file(path, ios::in | ios::binary);
    if (!file.is_open()) {return 1;};
    istream_iterator<uint8_t> start(file), end;
    file >> noskipws;
    vector<uint8_t> data(start, end);

//    for(int i = 0; i<data.size(); i++) { // just print all bytes from data as hex
//        phex(data[i]);
//    };

    uint8_t fsig[8]; copy_n(begin(data), 8, begin(fsig));
    uint16_t fver = ((uint16_t)data[8] << 8) | data[9];
    uint8_t name[128]; copy_n(next(begin(data), 10), 128, begin(name));
    uint8_t author[64]; copy_n(next(begin(data), 138), 64, begin(author));
    uint16_t timeS = ((uint16_t)data[202] << 8) | data[203];
    int8_t rootnote = static_cast<int8_t>(data[204]);
    uint16_t tempo = ((uint16_t)data[205] << 8) | data[206];
    uint8_t insc = data[207];
    uint8_t patc = data[208];
    cf::Instrument instruments[insc]; for(int i = 0; i<insc; i++) {
        instruments[i].type = data[209+(256*i)];
        copy_n(next(begin(data), 209+(256*1)+1), 255, begin(instruments[i].data));};
    cf::Pattern patterns[patc]; for(int i = 0; i<patc; i++) {
        patterns[i].locked = data[209+(256*insc)+(134*i)];
        patterns[i].muted = data[209+(256*insc)+(134*i)+1];
        patterns[i].prlen = data[209+(256*insc)+(134*i)+2];
        patterns[i].ofs = data[209+(256*insc)+(134*i)+3];
        patterns[i].profs = static_cast<int8_t>(data[209+(256*insc)+(134*i)+4]);
        patterns[i].iid = data[209+(256*insc)+(134*i)+5];
        for(int j = 0; j<cf::MPL; j++) {
            patterns[i].notes[j].volume = data[209+(256*insc)+(134*i)+6+(2*j)];
            patterns[i].notes[j].pitch = static_cast<int8_t>(data[209+(256*insc)+(134*i)+6+(2*j)+1]);};};
    uint8_t fend[64]; copy_n(next(begin(data), 209+(256*insc)+(134*patc)), 64, begin(fend));

    cout << "\033[0;7m"; for(int i = 0; i<8; i++) { phex(data[i]);}; // fsig
    cout << "\033[0;7;35m"; for(int i = 0; i<2; i++) {phex(data[8+i]);}; // ver
    cout << "\033[0;36m"; for(int i = 0; i<128; i++) {phex(data[10+i]);}; // name
    cout << "\033[0;34m"; for(int i = 0; i<64; i++) {phex(data[138+i]);}; // author
    cout << "\033[0;42m"; for(int i = 0; i<2; i++) {phex(data[202+i]);}; // time spent
    cout << "\033[0;41m"; phex(data[204]); // root note
    cout << "\033[0;43m"; for(int i = 0; i<2; i++) {phex(data[205+i]);}; // tempo
    cout << "\033[0;7;31m"; phex(data[207]); // insc
    cout << "\033[0;7;32m"; phex(data[208]); // patc
    cout << "\033[0;31m"; for(int i = 0; i<insc*256; i++) {phex(data[209+i]);}; // instruments
    cout << "\033[0;32m"; for(int i = 0; i<patc*134; i++) {phex(data[209+(256*insc)+i]);}; // patterns
    cout << "\033[0;7m"; for(int i = 0; i<64; i++) {phex(data[209+(256*insc)+(134*patc)+i]);}; // end
    cout << "\033[0m" << endl;

    return 0;
}
