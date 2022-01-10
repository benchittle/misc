#ifndef ArrayList_h
#define ArrayList_h

#define T int

typedef struct ArrayList ArrayList;


/* Append the value to the end of the ArrayList */
void ArrayList_append(ArrayList* list, T value);

/* Returns a new ArrayList. Caller must free. */
ArrayList* ArrayList_create();

/* Free memory associated with the given ArrayList */
void ArrayList_destroy(ArrayList* list);

/* Returns the integer at the given index in the array */
T ArrayList_get(ArrayList* list, size_t index);

/* Insert the value at the given index, shifting elements right as needed */
void ArrayList_insert(ArrayList* list, size_t index, T value);

/* Return the number of elements in the array */
size_t ArrayList_len(ArrayList* list);

/* Replace the value at the given index with the given new value */
void ArrayList_put(ArrayList* list, size_t index, T value);

/* Print the contents of the given ArrayList to STDOUT 
 * format: 
 */
void ArrayList_printf(ArrayList* list, const char* format);

/* Return a slice of the list. Uses Python syntax. */
ArrayList* ArrayList_slice(ArrayList* list, const char* sliceFormat);


#endif // ArrayList_h