
#include <stdio.h>
void calk(long number);
long max11=99999999999;
long max12=999999999999;
long max14=99999999999999;
long max13=9999999999999;
long max16=9999999999999999;
long max15=999999999999999;
int main(void)
{
    long number;
printf("Number: ");
scanf("%ld", &number);
    if (number<=max16 )
    {
        int n = number/max13;
        if(n==37 || n==34)
        {
           calk(number);
        }
    }
    else if (number<=max15)
    {
        int n = number/ max12;
        if(n==51 || n==52 || n==53 || n==54 || n==55)
        {
            calk(number);
        }

    }
    else if (number<=max14|| number<=max13)
    {
        int n = number/max11;
        if(n==4)
        {
            calk(number);
        }

    }
    else
    {
        printf("INVALID\n");
    }
    printf("INVALID\n");
    
    return 0;
}
void calk(long number){
    int i=0;
    int sum1=0;
    while(number>0)
    {    
        i++;
        long n = number%10;
        number=number/10;
        if(i%2==0)
        {
            n=n*2;
            if(n>9)
            {
                n=n%10+n/10;
            }
        }
        sum1+=n;
    }
    if(sum1%10==0)
    {
        printf("VALID\n");
    }
    else
    {
        printf("INVALID\n");
    }
}