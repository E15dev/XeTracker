rm -f ./player
g++ -std=c++11 -c player.cpp
g++ -std=c++11 player.o -o player -lsfml-audio -lsfml-system
rm -f ./player.o
