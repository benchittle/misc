#ifndef LinkedList_h
#define LinkedList_h

#include <stdlib.h>

#define T int

typedef struct LinkedList LinkedList;
typedef struct LinkedListNode LinkedListNode;

LinkedList* LinkedList_create();
void LinkedList_destroy(LinkedList* list);
T LinkedList_get(LinkedList* list, size_t index); 






#endif // LinkedList_h