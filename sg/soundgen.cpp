#include <iostream>
#include <vector>
#include <sstream>
#include <SFML/Audio.hpp>
#include "sg.h"

using namespace std;

int main() {
    float amp = 0.1;    // CHANGE IT LATER BUT ITS PAINFUL ON MAX VOL

    sf::SoundBuffer sb;
    vector<sf::Int16> samples;
    sf::Sound sp;

    string inp;
    vector<float> fq;
    float tmpv;


    while (1) {
        samples.clear();
        for (int i = 0; i < 44100; i++) { samples.push_back(sound::SineWave(i, 0, 0)); } // make sample 44100 long but full of 0s

        getline(cin, inp);
        istringstream iss(inp);

        fq.clear();
        while (iss >> tmpv) { fq.push_back(tmpv); }
        for (int j = 0; j < fq.size(); j++) {
            for (int i = 0; i < 44100; i++) {
                samples[i] += sound::SineWave(i, fq[j], amp);
            }
        }

        sb.loadFromSamples(&samples[0], samples.size(), 2, 44100);
        sp.setBuffer(sb);
        sp.setLoop(true);
        sp.play();
    }

    return 0;
}
