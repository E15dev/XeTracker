#include "p2f.hpp"

float p2f::convert(int p) {
    int oct = std::floor(p / 12.0);
    int mp = (12 + (p % 12)) % 12;
    return bfqs[mp]*std::pow(2, oct);
}
