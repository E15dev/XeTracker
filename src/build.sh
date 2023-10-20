clear
# remove stuff
echo -e "\033[7mclearing\033[0m"
rm -f ./player *.o
# compile stuff
echo -e "\033[7mcompiling: p2f\033[0m"
g++ -std=c++11 -c p2f.cpp
echo -e "\033[7mcompiling: sg\033[0m"
g++ -std=c++11 -c sg.cpp
echo -e "\033[7mcompiling: xetrproj\033[0m"
g++ -std=c++11 -c xetrproj.cpp
echo -e "\033[7mcompiling: player\033[0m"
g++ -std=c++11 -c player.cpp
# link stuff
echo -e "\033[7mlinking\033[0m"
g++ -std=c++11 player.o sg.o xetrproj.o p2f.o -o player -lsfml-audio -lsfml-system
# done
echo -e "\033[7mdone! i hope it works\033[0m"

