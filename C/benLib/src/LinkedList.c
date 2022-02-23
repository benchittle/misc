#include <stdio.h>
#include <stdlib.h>

#include "LinkedList.h"


struct LinkedListNode {
    LinkedListNode* next;
    T value;
};

struct LinkedList {
    size_t n;
    LinkedListNode* head;
    LinkedListNode* tail;
};
