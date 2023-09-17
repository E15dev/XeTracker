#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <algorithm>
#include <chrono>

#include "xetrproj.hpp"

#include <SFML/Audio.hpp>
#include "sg.h"
#include "p2f.hpp"

double getTime() {return std::chrono::duration<double>(std::chrono::system_clock::now().time_since_epoch()).count();}

int main(int argc, char *argv[0]) {
    if (argc<2) {
        printf("you need to specify filename\n"); // TODO: if not args, play in old mode (reading from stdin)
    } else {
        std::ifstream file(argv[1], std::ios::in | std::ios::binary);
        if (!file.is_open()) {return 1;};
        std::istream_iterator<uint8_t> start(file), end;
        file >> std::noskipws;
        std::vector<uint8_t> data(start, end);

        cf::Project cproj = cf::Project(data); // project from bytes

        printf("player started\n");

        float amp = 0.1;    // CHANGE IT LATER BUT ITS PAINFUL ON MAX VOL
        sf::SoundBuffer sb;
        std::vector<sf::Int16> samples;
        sf::Sound sp;
        sp.setLoop(true);

        double tn = getTime();
        int i = 0;
        while (1) {
            samples.clear();
            for (int i = 0; i < 44100; i++) { samples.push_back(0);} // make "samples" 44100 long (probably there is better way, but i have no internet to check)

            for (uint8_t j = 0; j<cproj.getPatternCount(); j++) {
                cf::Note cnote = cproj.playerRead(j, i);
                if (!cproj.getPattern(j).muted and cnote.volume > 0) { // ignore muted patterns and notes
                    for (int i = 0; i < 44100; i++) {
                        samples[i] += waveforms::fromInstrument(i, p2f::convert(cnote.pitch), amp*cnote.volume/255, cproj.getInstrument(cproj.getPattern(j).iid));
                    };
                };
            };

            while (getTime()-tn < i*(60.0/cproj.tempo)) {} // waiting for for next note until before changing sample again
            sb.loadFromSamples(&samples[0], samples.size(), 2, 44100);
            sp.setBuffer(sb);
            sp.play();

            i = i + 1;
        }
    }
    return 0;
}
