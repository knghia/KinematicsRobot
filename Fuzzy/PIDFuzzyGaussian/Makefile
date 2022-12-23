
all: build show

build:
	g++ -Wall -g -c ./fuzzy.cpp -o ./fuzzy.o -I./fuzzy.h
	g++ -Wall -g -c ./main.cpp -o ./main.o -I./main.h
	g++ main.o fuzzy.o -lm -o main
	
show:
	C:/Users/Admin/AppData/Local/Programs/Python/Python36/python.exe e:/KinematicsRobot/Fuzzy/PIDFuzzyGaussian/main.py