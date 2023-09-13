rm -f ./cfv
g++ -std=c++11 -c cfv.cpp
g++ -std=c++11 cfv.o -o cfv -lsfml-audio -lsfml-system
rm -f ./cfv.o
