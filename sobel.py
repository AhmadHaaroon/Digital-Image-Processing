#Import Libraries
import numpy as np

#Import Files
from input import input_text
import convolution
import padding as pad

#Sobel filter
def sobel_filter(image_array,direction='Horizontal',padding=None):
    if(image_array.ndim == 3):
        new_image_array = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0])))
    elif(image_array.ndim == 2):
        new_image_array = np.zeros((len(image_array),len(image_array[0])))
    filter=None

    #Select padding type, if none set
    if(padding==None):
        option = input_text("Select padding type:\n1)Zero Padding\n\nOption Selected:",1)
        if(option == 1):
            image_array = pad.zero_padding(image_array,3)
    else:
        #Padding image
        image_array = pad.zero_padding(image_array,3)

    #Set sobel matrix
    if(direction=='Horizontal'):
        filter = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    else:
        filter = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

    #Now apply filter on image
    new_image_array = convolution.convolution(image_array,new_image_array,filter)
    
    return new_image_array