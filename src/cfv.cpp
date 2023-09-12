#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <algorithm>
#include <chrono>
#include "xetrproj.hpp"
#include "p2f.hpp"

void phex(uint8_t b) { printf("%02x ", b); }

double getTime() {return std::chrono::duration<double>(std::chrono::system_clock::now().time_since_epoch()).count();}

int main(int argc, char *argv[0]) {
    if (argc<2) {printf("you need to specify filename\n"); exit(0);}

    std::ifstream file(argv[1], std::ios::in | std::ios::binary);
    if (!file.is_open()) {return 1;};
    std::istream_iterator<uint8_t> start(file), end;
    file >> std::noskipws;
    std::vector<uint8_t> data(start, end);

    cf::Project cproj = cf::Project(data); // project from bytes

    double tn = getTime();
    int i = 0;
    while (1) {
        while (getTime()-tn < i*(60.0/cproj.tempo)) {}
        cf::Note cnote = cproj.playerRead(0, i);
        // TODO: DO FOR ALL PATTERNS NOT ONLY FIRST
        printf("%d %f 0 0", cnote.volume, p2f::convert(cnote.pitch));
        printf("\n"); fflush(stdout);
        i = i + 1;
    }

    return 0;
}
