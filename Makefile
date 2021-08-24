LINKS = -ltgui -lsfml-graphics -lsfml-window -lsfml-system
SFML_DIR = C:/Program Files (x86)/SFML
TGUI_DIR = C:/Program Files (x86)/TGUI

all: compile link run clean

compile:
	g++ -c src/main.cpp -o bin/main.o -I"$(SFML_DIR)/include" -I"$(TGUI_DIR)/include"
	g++ -c src/PerlinNoise.cpp -o bin/PerlinNoise.o

link:
	g++ bin/*.o -o bin/main.exe -L"$(SFML_DIR)/lib" -L"$(TGUI_DIR)/lib" $(LINKS)

clean:
	rm -rf bin/*.o
	rm -rf bin/*.exe

run:
	bin/main.exe
