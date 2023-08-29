#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <algorithm>
#include "xetrproj.h"

using namespace std;

int main()
{
    string path;
    getline(cin, path);
    ifstream file(path);
    if (!file.is_open()) {return 1;};
    istream_iterator<uint8_t> start(file), end;
    vector<uint8_t> data(start, end);

    uint8_t fsig[8]; copy_n(begin(data), 8, begin(fsig));
    uint16_t fver = ((uint16_t)data[8] << 8) | data[9];
    uint8_t name[128]; copy_n(next(begin(data), 10), 128, begin(name));
    uint8_t author[64]; copy_n(next(begin(data), 138), 64, begin(author));
    uint16_t timeS = ((uint16_t)data[202] << 8) | data[203];
    int8_t rootnote = static_cast<int8_t>(data[204]); // should be signed, idk if it is check it later TODO
    uint16_t tempo = ((uint16_t)data[205] << 8) | data[206];
    uint8_t insc = data[207];
    uint8_t patc = data[208];
    cf::Instrument instruments[insc];
    cf::Pattern patterns[patc];
    // TODO: IDK HOW, READ REST OF STUFF TO INSTUMENTS AND PATTERNS

    cout << "\033[0;7m"; for(int i = 0; i<8; i++) { cout << hex << (int)data[i] << " ";}; // fsig
    cout << "\033[0;7;35m"; for(int i = 0; i<2; i++) {cout << hex << (int)data[8+i] << " ";}; // ver
    cout << "\033[0;36m"; for(int i = 0; i<128; i++) {cout << hex << (int)data[10+i] << " ";}; // name
    cout << "\033[0;34m"; for(int i = 0; i<64; i++) {cout << hex << (int)data[138+i] << " ";}; // author
    cout << "\033[0;42m"; for(int i = 0; i<2; i++) {cout << hex << (int)data[202+i] << " ";}; // time spent
    cout << "\033[0;41m"; cout << hex << (int)data[204] << " "; // root note
    cout << "\033[0;43m"; for(int i = 0; i<2; i++) {cout << hex << (int)data[205+i] << " ";}; // tempo
    cout << "\033[0;7;31m"; cout << hex << (int)data[207] << " "; // insc
    cout << "\033[0;7;32m"; cout << hex << (int)data[208] << " "; // patc
    cout << "\033[0;31m"; for(int i = 0; i<insc*256; i++) {cout << hex << (int)data[209+i] << " ";}; // instruments
    cout << "\033[0;32m"; for(int i = 0; i<patc*134; i++) {cout << hex << (int)data[209+(256*insc)+i] << " ";}; // patterns
    cout << "\033[0;7m"; for(int i = 0; i<64; i++) {cout << hex << (int)data[209+(256*insc)+(134*patc)+i] << " ";}; // end

    cout << "\033[0m" << endl;
    return 0;
}
