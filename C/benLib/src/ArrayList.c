#include "ArrayList.h"
#include <stdio.h>
#include <stdlib.h>



// Print given message with file name and line before exiting the program
#define _errorExit(msg) printf("ERROR in %s @ %d: %s\n", __FILE__, __LINE__, msg); \
                        exit(EXIT_FAILURE);

// Print given message with file name and line, call perror, and exit the program
#define _perrorExit(msg)    printf("%s @ %d: ", __FILE__, __LINE__); \
                            perror(msg);                             \
                            exit(EXIT_FAILURE);

struct ArrayList {
    size_t length; // Length of internal array
    size_t n;    // Number of elements in array
    T* array;  // Array pointer 
};

void __errorExit(char* msg, char* filename, int line);
void __perrorExit(char* msg, char* filename, int line);

void _ArrayList_grow(ArrayList* list); 
void _ArrayList_shrink(ArrayList* list);


ArrayList* ArrayList_create() {
    ArrayList* list = malloc(sizeof(ArrayList)); // Fails?
    list->length = 128;
    list->n = 0;
    list->array = malloc(list->length * sizeof(*list->array)); // Fails?
    return list;
}

void ArrayList_destroy(ArrayList* list) {
    free(list->array); // Fails?
    free(list);
}

T ArrayList_get(ArrayList* list, size_t index) {
    if (index >= list->n) {
        _errorExit("List index out of range");
    }
    return list->array[index];
}

void ArrayList_insert(ArrayList* list, size_t index, T value) {
    if (index >= list->n) {
        _errorExit("List index out of range");
    }
    if (list->n + 1 == list->length) {
        _ArrayList_grow(list);
    }

    // Shift elements right to make room at the insertion index
    for (size_t i = list->n; i >= index; i--) {
        list->array[i] = list->array[i - 1];
    }
    list->array[index] = value;
    list->n++;
}


void ArrayList_put(ArrayList* list, size_t index, T value) {
    if (index >= list->n) {
        _errorExit("List index out of range");
    }

    list->array[index] = value;
}

/* Append the value to the end of the ArrayList */
void ArrayList_append(ArrayList* list, T value) {
    if (list->n + 1 == list->length) {
        _ArrayList_grow(list);
    }

    list->array[list->n] = value;
    list->n++;
}

void ArrayList_printf(ArrayList* list, const char* format) {
    printf("ArrayList[");
    if (list->n > 0) {
        printf(format, list->array[0]);
        for (size_t i = 1; i < list->n; i++) {
            printf(", ");
            printf(format, list->array[i]);
        }
    }
    puts("]");
}


/* Double the length of the internal array of an ArrayList */
void _ArrayList_grow(ArrayList* list) {
    list->length *= 2;
    T* tmp = realloc(list->array, list->length * sizeof(*list->array));
    if (tmp == NULL) {
        free(list->array);
        _perrorExit("\0");
    } else {
        list->array = tmp;
    }
}

/* Halve the length of the internal array of an ArrayList */
void _ArrayList_shrink(ArrayList* list) {
    list->length /= 2;
    T* tmp = realloc(list->array, list->length * sizeof(*list->array));
    if (tmp == NULL) {
        free(list->array);
        _perrorExit("\0");
    } else {
        list->array = tmp;
    }
}