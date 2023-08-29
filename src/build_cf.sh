rm -f ./cf
g++ -std=c++11 -c cf.cpp
g++ -std=c++11 cf.o -o cf
rm -f ./cf.o
