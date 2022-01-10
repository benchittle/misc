#include <stdio.h>

#include "ArrayList.h"

int main(void) {
    ArrayList* list = ArrayList_create();
    for (int i = -5; i < 10; i++) {
        ArrayList_append(list, i);
    }
    ArrayList_print(list, "%d");

    ArrayList_destroy(list);
}