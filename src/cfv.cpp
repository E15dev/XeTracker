#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <algorithm>
#include "xetrproj.hpp"

void phex(uint8_t b) { printf("%02x ", b); }

int main(int argc, char *argv[0]) {
    if (argc<2) {printf("you need to specify filename\n"); exit(0);}

    std::ifstream file(argv[1], std::ios::in | std::ios::binary);
    if (!file.is_open()) {return 1;};
    std::istream_iterator<uint8_t> start(file), end;
    file >> std::noskipws;
    std::vector<uint8_t> data(start, end);

    cf::Project proj = cf::Project(data);

    for(int i = 0; i<data.size(); i++) { // just print all bytes from data as hex
        phex(data[i]);
    };

    return 0;
}
