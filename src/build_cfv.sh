rm -f ./cfv
g++ -std=c++11 -c cfv.cpp
g++ -std=c++11 cfv.o -o cfv
rm -f ./cfv.o
