#Import Libraries
import numpy as np

#Convolution function
def convolution(image_array,new_image_array,matrix):
    size = len(matrix)
    for i in range(len(new_image_array)):
        for j in range(len(new_image_array[0])):
            for k in range(size):
                for l in range(size):
                    if(image_array.ndim == 3):
                        for m in range(len(new_image_array[0][0])):
                            new_image_array[i][j][m] += image_array[i+k][j+l][m] * matrix[k][l]
                    elif(image_array.ndim == 2):
                        new_image_array[i][j] += image_array[i+k][j+l] * matrix[k][l]
    return new_image_array