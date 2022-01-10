#include <stdio.h>
//#define ACC 4

double squareroot(double n, int acc) {
    double x = n > 0 ? 1 : -1;
    
    for (int i = 0; i < acc; i++) {
        //x = x - (x * x - n) / (2 * x);
        x = (x + n / x) / 2;
    }
    return x;
}


int main(void) {
    double num = 5;
    for (int i = 1; i < 10; i++) {
        printf("sqrt(%g) = %lf (acc=%d)\n", num, squareroot(num, i), i);
    }
}