#include <stdio.h>
#include <ctype.h>

int main(void)
{
    char player1[100];
    char player2[100];

    printf("Player 1: ");
    scanf("%99s", player1);

    printf("Player 2: ");
    scanf("%99s", player2);

    int sum1 = 0;
    int sum2 = 0;
    int temp = 0;

    char *p1 = player1;
    char *p2 = player2;

    while (*p1 != '\0')
    {
        temp = toupper(*p1) - 'A' + 1;

        if (temp >= 1 && temp <= 26)
        {
            sum1 += temp;
        }

        p1++;
    }

    while (*p2 != '\0')
    {
        temp = toupper(*p2) - 'A' + 1;

        if (temp >= 1 && temp <= 26)
        {
            sum2 += temp;
        }

        p2++;
    }

    if (sum1 > sum2)
    {
        printf("Player 1 wins!\n");
    }
    else if (sum2 > sum1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}