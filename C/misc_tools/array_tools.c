#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

void iswap(int* n1, int* n2) {
    int tmp = *n1;
    *n1 = *n2;
    *n2 = tmp;
}

int imax(int* arr, size_t size) {
    int n = arr[0];
    for (int i = 1; i < size; i++) {
        if (n < arr[i]) {
            n = arr[i];
        }
    }
    return n;
}

int imin(int* arr, size_t size) {
    int n = arr[0];
    for (int i = 1; i < size; i++) {
        if (n < arr[i]) {
            n = arr[i];
        }
    }
    return n;
}

int* isort(int* arr, int size, bool ascending) {
    int tmp;
    if (ascending) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size - i - 1; j++) {
                if (arr[j] > arr[j + 1]) { 
                    tmp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = tmp;
                }
            }
        }
    } else {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size - i - 1; j++) {
                if (arr[j] < arr[j + 1]) {
                    tmp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = tmp;
                }
            }
        }
    }
    return arr;
}

int* ishuffle(int* arr, size_t size) {
    srand(time(NULL));
    for (int i = 0; i < size; i++) {
        iswap(&arr[rand() % size], &arr[rand() % size]);
    }
    return arr;
}
