#include<stdio.h>
int main(){
    int n;
    scanf("%d",&n);
    int total=0;
    if(n>=100){
        total+=n/100;
        n=n%100;
    }
    if(n>=25){
        total+=n/25;
        n=n%25;
    }
    if(n>=10){
        total+=n/10;
        n=n%10;
    }
    if(n>=5){
        total+=n/5;
        n=n%5;
    }
    total+=n;
    printf("%d\n",total);
}