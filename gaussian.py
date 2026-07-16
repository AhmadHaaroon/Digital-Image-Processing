#Import Libraries
import numpy as np

#Import files
from input import input_text
import convolution
import padding as pad

#Gaussian filter
def gaussian_filter(image_array, sigma=None, size=None, padding=None):
    if(image_array.ndim == 3):
        new_image_array = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0])))
    elif(image_array.ndim == 2):
        new_image_array = np.zeros((len(image_array),len(image_array[0])))

    #Select sigma, if none set
    if(sigma==None):
        sigma = float(input("Enter the value of the blur spread (sigma):"))
        print()

    #Select size, if none set
    if(size==None):
        size = float(input("Enter the size of the kernel:"))
        print()

    #Select padding type, if none set
    if(padding==None):
        option = input_text("Select padding type:\n1)Zero Padding\n\nOption Selected:",1)
        if(option == 1):
            image_array = pad.zero_padding(image_array,size)
    else:
        #Padding image
        image_array = pad.zero_padding(image_array,size)

    #Calculate the gaussian matrix
    gaussian_matrix = gaussian_matrix_calculation(sigma,size)

    #Converting it to normalized, integer approximation
    gaussian_matrix = gaussian_matrix/np.sum(gaussian_matrix)
    gaussian_matrix = np.round(gaussian_matrix/gaussian_matrix[0][0])
    gaussian_matrix = gaussian_matrix/np.sum(gaussian_matrix)

    #Now apply filter on image
    new_image_array = convolution.convolution(image_array,new_image_array,gaussian_matrix)
                    
    return new_image_array

def gaussian_matrix_calculation(sigma=None, size=None):
    gaussian_matrix = (np.zeros((size,size))).astype(np.float128)
    for i in range(-int(size/2), int(size/2)+1):
        for j in range(-int(size/2), int(size/2)+1):
            power_value = np.exp(-((i**2)+(j**2))/(2*sigma**2))
            gaussian_matrix[i + int(size/2)][j + int(size/2)] = power_value

    return gaussian_matrix