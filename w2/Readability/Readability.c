#include <stdio.h>
#include <ctype.h>

int main(void)
{
    char text[1000];

    printf("Text: ");
    fgets(text, sizeof(text), stdin);

    int letters = 0;
    int words =1;
    int sentences = 0;
    int count = 0;

    while (text[count] != '\0')
    {
        if (tolower(text[count]) >= 'a' && tolower(text[count]) <= 'z')
        {
            letters++;
        }

        if (text[count] == ' ')
        {
            words++;
        }

        if (text[count] == '.' || text[count] == '!' || text[count] == '?')
        {
            sentences++;
        }

        count++;
    }

    float L = ((float) letters / words) * 100;
    float S = ((float) sentences / words) * 100;

    float grade = 0.0588 * L - 0.296 * S - 15.8;
    int grades = grade;

    if (grade - grades >= 0.5)
    {
        grades++;
    }

    

    if (grades < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grades >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grades);
    }

    return 0;
}