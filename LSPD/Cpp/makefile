all:
	g++ -Wall -g -c ./LSPB.cpp -o ./LSPB.o -I./LSPB.h
	g++ -Wall -g -c ./main.cpp -o ./main.o -I./main.h
	g++ main.o LSPB.o -lm -o main
	./main.exe