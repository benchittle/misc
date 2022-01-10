CC=gcc
CFLAGS=-g -Wall

SRCS=$(wildcard src/*.c)
OBJS=$(patsubst src/%.c, obj/%.o, $(SRCS))

all: $(OBJS)

obj/%.o: src/%.c src/%.h
	$(CC) $(CFLAGS) -c $< -o $@

ArrayListTest: tests/ArrayListTest.c obj/ArrayList.o
	$(CC) $(CFLAGS) -Isrc $^ -o bin/$@

clean:
	rm -rf bin/* obj/*