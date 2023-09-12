#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <algorithm>
#include "xetrproj.hpp"

void phex(uint8_t b) { printf("%02x ", b); }

int main() {
    std::string path;
    getline(std::cin, path);
    std::ifstream file(path, std::ios::in | std::ios::binary);
    if (!file.is_open()) {return 1;};
    std::istream_iterator<uint8_t> start(file), end;
    file >> std::noskipws;
    std::vector<uint8_t> data(start, end);

    cf::Project proj = cf::Project(data);
//    std::cout << static_cast<uint16_t>(proj.getPattern(3).notes[1].pitch)<< std::endl;

    return 0;
}
