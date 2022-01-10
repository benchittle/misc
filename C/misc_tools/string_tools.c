#include "string_tools.h"
#include <stdio.h>
#include <stdlib.h>

/* Returns the length of the given string up to the first string terminator. */
size_t slen(char *string) {
    size_t len = 0;
    while (*string++ != '\0') {
        len++;
    }
    return len;
}

char* scopy(char* dest, char* string) {
    char* dest_copy = dest;
    while (*string != '\0') {
        *dest++ = *string++;
    }
    *dest = '\0';
    return dest_copy;
}

// Implement negative indexing?
char* sslice(char* dest, char* string, size_t start, size_t stop, size_t skip) {
    char* dest_copy = dest;
    for (size_t i = start; i < stop; i += skip) {
        *dest++ = string[i];
    }
    *dest = '\0';
    return dest_copy;
}

int sindexc(char* string, char c, size_t start) {
    string = &string[start];
    char* string_copy = string;
    while (*string != '\0') {
        if (*string++ == c) {
            return string - string_copy - 1 + start;
        }
    }
    return -1;
}

int sindexs(char* string, char* sub, size_t start) {
    string = &string[start];
    char* string_copy = string;
    char* sub_copy = sub;
    while (*string != '\0') {
        while (*string++ == *sub++) {
            if (*sub == '\0') {
                return string - string_copy - slen(sub_copy) + start;
            }
        }
        sub = sub_copy;
    }
    return -1;
}

int int_to_str(char* dest, int n) {
    // dest must be a string 2 bigger than the length of n
    int n_ = n < 0 ? -n : n;
    char* dest_ = dest;
    do {
        *dest_++ = '0' + n_ % 10;
        n_ /= 10;}
    while (n_ != 0);
    
    int size = dest_ - dest;
    char tmp;
    for (int i = 0; i < size / 2; i++) {
        tmp = dest[i];
        dest[i] = dest[size - i - 1];
        dest[size - i - 1] = tmp;
    }
    *dest_ = '\0';
    if (n < 0) {
        dest_++;
        while (dest_ != dest) {
            *dest_-- = *dest_;
        }
        *dest_ = '-';
    }
    return size;
}

int scountc(char* string, char c) {
    int count = 0;
    while (*string != '\0') {
        if (*string++ == c) {
            count++;
        }
    } 
    return count;
}

int scounts(char* string, char* sub) {
    int count = 0;
    char* sub_copy = sub;
    while (*string != '\0') {
        while (*string++ == *sub++) {
            if (*sub == '\0' && *string != '\0') {
                count++;
                break;
            }
        }
        sub = sub_copy;
    }
    return count;
}


//strip first or else it will cause rror when a sep is a the end of a string
char* split(char* string, char* sep) {
    size_t string_length = slen(string);
    size_t sep_length = slen(sep);
    size_t sep_count = scounts(string, sep);
    // Array for storing the positon of each separator found in the parent
    // string. 
    size_t sep_indices[sep_count + 2];

    // Find the position of each separator in the string. Index 0 and the last
    // index position are also included.
    sep_indices[0] = 0;
    sep_indices[1] = sindexs(string, sep, 0);
    for (size_t i = 2; i < sep_count + 1; i++) {
        sep_indices[i] = sindexs(string, sep, sep_indices[i - 1] + sep_length);
    }
    // Uses 1 higher than the last index position to mimic a separator being
    // present at the end of the string.
    sep_indices[sep_count + 1] = string_length;

    // Get the largest gap between consecutive separators; this is the array
    // size necessary for each substring.
    size_t max_dif = sep_indices[1];
    for (size_t i = 2; i < sep_count + 1; i++) {
        size_t dif = sep_indices[i] - sep_indices[i - 1];
        if (dif > max_dif) {
            max_dif = dif - sep_length;
        }
    }
    // Account for the string terminator.
    max_dif++;

    // 2D array for storing the substrings.
    char split_string[sep_count + 1][max_dif + 1];
    // Slice out each substring. The first slice does not need to account for a
    // separator being present, so it is done first outside the loop.
    sslice(split_string[0], string, 0, sep_indices[1], 1);
    for (size_t i = 1; i < sep_count + 1; i++) {
        sslice(split_string[i], string, sep_indices[i] + sep_length, sep_indices[i + 1], 1);
    }

    for (int i = 0; i < sep_count + 1; i++) {
        printf("%s\n", split_string[i]);
    }
}

short startswith(char* string, char* sub) {
    while (*string++ == *sub++) {
        if (*sub == '\0') {
            return 1;
        }
    }
    return 0;
}

// optimize
short endswith(char* string, char* sub) {
    size_t string_length = slen(string);
    size_t sub_length = slen(sub);
    if (sub_length >= string_length) {
        string += string_length - sub_length;
        while (*string++ == *sub++) {
            if (*sub == '\0') {
                return 1;
            }
        }
    }
    return 0;
}


//split
//join

int main(void) {
    char* str = "  hey you, yeahhhhh you";
    printf("%d", endswith("", "you"));
    //split(str, " ");
}