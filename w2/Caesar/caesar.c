#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, char *argv[])
{
    // TODO: check argc == 2
    if (argc != 2)
    {
        printf("must provide a single command-line argument\n");
        return 1;
    }

    // TODO: validate argv[1] is numeric
    if (isdigit(argv[1][0]) == 0)
    {
        printf("must provide a numeric command-line argument\n");
        return 1;
    }
    // TODO: convert key using atoi
    int key = atoi(argv[1]);
    // TODO: read plaintext
    char text[1000];
    printf("plaintext: ");
    scanf("%[^\n]%*c", text);

    // TODO: rotate characters
    for (int i=0; text[i] != '\0'; i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                text[i] = ((text[i] - 'A' + key) % 26) + 'A';
            }
            else
            {
                text[i] = ((text[i] - 'a' + key) % 26) + 'a';
            }
        }
    }

    printf("ciphertext: %s\n", text);
    return 0;
}