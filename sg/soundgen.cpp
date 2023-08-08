#include <iostream>
#include <SFML/Audio.hpp>
#include <vector>
#include "sg.h"

using namespace std;

int main() {
    float amp = 0.1;    // CHANGE IT LATER BUT ITS PAINFUL ON MAX VOL

    sf::SoundBuffer sb;
    vector<sf::Int16> samples;
    sf::Sound sp;

    double fq;
    double lfq = 0;
    while (1) {
        cin>>fq;
        if (fq != lfq) {
            samples.clear();
            for (int i = 0; i < 44100; i++) {
                samples.push_back(sound::SineWave(i, fq, amp));
            }

            sb.loadFromSamples(&samples[0], samples.size(), 2, 44100);
            sp.setBuffer(sb);
            sp.setLoop(true);
            sp.play();
        }
        lfq = fq;
    }

    return 0;
}
