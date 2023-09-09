#include <iostream>
#include <vector>
#include <sstream>
#include <SFML/Audio.hpp>
#include "sg.h"

int main() {
    float amp = 0.1;    // CHANGE IT LATER BUT ITS PAINFUL ON MAX VOL

    sf::SoundBuffer sb;
    std::vector<sf::Int16> samples;
    sf::Sound sp;
    sp.setLoop(true);

    std::string inp;
    std::vector<float> vals;
    float tmpv;

    while (1) {
        samples.clear();
        for (int i = 0; i < 44100; i++) { samples.push_back(0);} // make "samples" 44100 long (probably there is better way, but i have no internet to check)
        getline(std::cin, inp);
        std::istringstream iss(inp);

        vals.clear();
        while (iss >> tmpv) { vals.push_back(tmpv); }
        for (int j = 0; j < vals.size()/4; j++) {
            if (vals[j*4] != 0.0) { // ignore if volume is 0
                for (int i = 0; i < 44100; i++) { samples[i] += waveforms::Sine(i, vals[(j*4)+1], amp*vals[j*4]); }
            }
        }

        sb.loadFromSamples(&samples[0], samples.size(), 2, 44100);
        sp.setBuffer(sb);
        sp.play();
    }

    return 0;
}
