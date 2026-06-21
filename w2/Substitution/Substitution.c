#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_TEXT 1024

int main(int argc, char *argv[])
{
    if (argc != 2 || strlen(argv[1]) != 26)
    {
        printf("not complete 1\n");
        return 1;
    }

    // validate key: alphabetic + no duplicates
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha((unsigned char)argv[1][i]))
        {
            printf("not complete 2\n");
            return 1;
        }

        for (int j = i + 1; j < (26-i+1); j++)
        {
            if (argv[1][i] == argv[1][j])
            {
                printf("not complete 3  \n");
                return 1;
            }
        }
    }

    char key[27];
    strcpy(key, argv[1]);

    char text[MAX_TEXT];

    printf("plaintext: ");
    if (!fgets(text, sizeof(text), stdin))
    {
        return 1;
    }

    // remove newline if present
    text[strcspn(text, "\n")] = '\0';

    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isalpha((unsigned char)text[i]))
        {
            if (isupper((unsigned char)text[i]))
            {
                text[i] = toupper((unsigned char)key[text[i] - 'A']);
            }
            else
            {
                text[i] = tolower((unsigned char)key[text[i] - 'a']);
            }
        }
    }

    printf("ciphertext: %s\n", text);
    return 0;
}