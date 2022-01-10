#ifndef STRING_TOOLS_H_
# define STRING_TOOLS_H_
# include <stddef.h>

size_t slen(char *string);
char* scopy(char* dest, char* string);
char* sslice(char* dest, char* string, size_t start, size_t stop, size_t skip);
int sindexc(char* string, char c, size_t start);
int sindexs(char* string, char* sub, size_t start);
int int_to_str(char* dest, int n);
int scountc(char* string, char c);
int scounts(char* string, char* sub);
char* split(char* string, char* sep);
short startswith(char* string, char* sub);
short endswith(char* string, char* sub);

#endif // STRING_TOOLS_H_