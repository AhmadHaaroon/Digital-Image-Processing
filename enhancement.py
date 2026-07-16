#Import Libraries
import numpy as np

#Import files
from input import input_text

#Enhancement Function
def enhancement(image_array):
    #Check enhancement method
    option = input_text("Which enhancement do you wish to perform?:\n1)Negative Image\n2)Thresholding\n\n" \
                    "Option Selected:",2)

    #Create new array
    if(image_array.ndim == 3):
        new_image_array = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0])))
    elif(image_array.ndim == 2):
        new_image_array = np.zeros((len(image_array),len(image_array[0])))

    #Assign values based on method
    if(option==1):
        new_image_array = negative(image_array)
    if(option==2):
        midpoint=None
        while(midpoint==None):
            try:
                midpoint = float(input("Enter the midpoint/threshold value: "))
                print()
            except:
                midpoint=None
                print("\nInvalid value.\n")

        spread=None
        while(spread==None):
            try:
                spread = float(input("Enter the spread value: "))
                print()
            except:
                spread=None
                print("\nInvalid value.\n")

        new_image_array = threshold(image_array,midpoint,spread)
    return new_image_array

#Negative
def negative(image_array):
    #Function: y = -x + 255
    return -image_array + 255

#Threshold
def threshold(image_array,midpoint,spread):
    if(spread==0):
        return np.where(image_array>midpoint,255,0)
    return 255/(1+np.exp(-((image_array-midpoint)/spread)))