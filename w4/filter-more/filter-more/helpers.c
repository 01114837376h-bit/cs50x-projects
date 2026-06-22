#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Get average of RGB values
            int average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3;

            // Set RGB values to average
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swap pixels
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0;i<height;i++){
        for(int j=0;j<width;j++){
            // Get average of surrounding pixels
            int redSum = 0, greenSum = 0, blueSum = 0, count = 0;
            for (int di = -1; di <= 1; di++){
                for (int dj = -1; dj <= 1; dj++){
                    int ni = i + di, nj = j + dj;
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width){
                        
                        redSum += image[ni][nj].rgbtRed;
                        greenSum += image[ni][nj].rgbtGreen;
                        blueSum += image[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }
            // Set pixel to average color
            image[i][j].rgbtRed = redSum / count;
            image[i][j].rgbtGreen = greenSum / count;
            image[i][j].rgbtBlue = blueSum / count;

        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
        for (int i=0;i<height;i++){
            for(int j=0;j<width;j++){
                // Get Gx and Gy values
                int GxRed = 0, GxGreen = 0, GxBlue = 0;
                int GyRed = 0, GyGreen = 0, GyBlue = 0;
                for (int di = -1; di <= 1; di++){
                    for (int dj = -1; dj <= 1; dj++){
                        int ni = i + di, nj = j + dj;
                        if (ni >= 0 && ni < height && nj >= 0 && nj < width){
                            int weightX = (dj == -1) ? -1 : (dj == 1) ? 1 : 0;
                            int weightY = (di == -1) ? -1 : (di == 1) ? 1 : 0;
                            
                            GxRed += image[ni][nj].rgbtRed * weightX;
                            GxGreen += image[ni][nj].rgbtGreen * weightX;
                            GxBlue += image[ni][nj].rgbtBlue * weightX;
    
                            GyRed += image[ni][nj].rgbtRed * weightY;
                            GyGreen += image[ni][nj].rgbtGreen * weightY;
                            GyBlue += image[ni][nj].rgbtBlue * weightY;
                        }
                    }
                }
                // Set pixel to magnitude of Gx and Gy
                image[i][j].rgbtRed = fmin(255, round(sqrt(GxRed * GxRed + GyRed * GyRed)));
                image[i][j].rgbtGreen = fmin(255, round(sqrt(GxGreen * GxGreen + GyGreen * GyGreen)));
                image[i][j].rgbtBlue = fmin(255, round(sqrt(GxBlue * GxBlue + GyBlue * GyBlue)));
    
            }
        }
    return;
}
