#include <stdio.h>

int main() {
    char name[100];

    scanf("%99s", name);

    printf("hello ");
    printf("%s", name);
    printf("\n");

    return 0;
}