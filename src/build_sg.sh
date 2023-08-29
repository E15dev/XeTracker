rm -f ./sg
g++ -std=c++11 -c soundgen.cpp
g++ -std=c++11 soundgen.o -o soundgen -lsfml-audio -lsfml-system
rm -f ./soundgen.o

