all:
	g++ -Wall -g -c ./fuzzy.cpp -o ./fuzzy.o -I./fuzzy.h
	g++ -Wall -g -c ./main.cpp -o ./main.o -I./main.h
	g++ main.o fuzzy.o -lm -o main
	./main.exe