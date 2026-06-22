#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
 
int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf( "Usage: ./recover image\n");
        return 1;
    }
    char *infile = argv[1];
    FILE *inptr = fopen(infile, "rb");
    if (inptr == NULL)
    {
        printf( "Could not open %s.\n", infile);
        return 2;
    }
    FILE *outptr = NULL;
    char *outfile = argv[2];
    uint8_t buffer[512];
    int file_count = 0;
    while (fread(buffer, sizeof(uint8_t), 512, inptr) == 512)
    {
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xF0) == 0xE0)
        {
            file_count++;
            sprintf(outfile, "%03i.jpg", file_count);
            outptr = fopen(outfile, "wb");
            if (outptr == NULL)
            {
                printf( "Could not create %s.\n", outfile);
                return 3;
            }

        }
        if (file_count > 0)
        {
            fwrite(buffer, sizeof(uint8_t), 512, outptr);

        }
    }


 
}