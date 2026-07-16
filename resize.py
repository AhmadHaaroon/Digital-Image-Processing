#Import Libraries
import numpy as np

#Import files
from input import input_text

#Resize Function
def resize(image_array):
    #Check resize method
    option = input_text("Which resize do you wish to perform?:\n1)Nearest Neighbour\n2)Bilinear\n\n" \
                "Option Selected:",2)

    #Get resize amount
    width=-1
    while(width<=0):
        try:
            width = int(input("Enter new width of image: "))
            if(width<=0):
                print("\nInvalid option entered, please try again.\n")
            else:
                print()
        except:
            print("\nInvalid option entered, please try again.\n")
    
    height=-1
    while(height<=0):
        try:
            height = int(input("Enter new width of image: "))
            if(height<=0):
                print("\nInvalid option entered, please try again.\n")
            else:
                print()
        except:
            print("\nInvalid option entered, please try again.\n")

    #Create new array
    if(image_array.ndim == 3):
        new_image_array = np.zeros((width,height,len(image_array[0][0])))
    elif(image_array.ndim == 2):
        new_image_array = np.zeros((width,height))

    #Assign values based on method
    if(option==1):
        image_array = nearest_neighbour(image_array,new_image_array)
    elif(option==2):
        image_array = bilinear(image_array,new_image_array)
    return image_array


#Nearest Neighbour
def nearest_neighbour(image_array,new_image_array):
    #Get scales
    scalex = len(new_image_array[0])/len(image_array[0])
    scaley = len(new_image_array)/len(image_array)

    #Assign values
    for i in range(len(new_image_array)):
        for j in range(len(new_image_array[0])):
            if(image_array.ndim == 3):
                for k in range(len(new_image_array[0][0])):
                    new_image_array[i,j,k] = image_array[min(int(round(i / scaley)), len(image_array) - 1), min(int(round(j / scalex)), len(image_array[0]) - 1), k]
            elif(image_array.ndim == 2):
                new_image_array[i,j] = image_array[min(int(round(i / scaley)), len(image_array) - 1), min(int(round(j / scalex)), len(image_array[0]) - 1)]

    return new_image_array

#Bilinear
def bilinear(image_array,new_image_array):
    #Get scales
    scalex = len(new_image_array[0])/len(image_array[0])
    scaley = len(new_image_array)/len(image_array)

    #Assign values
    for i in range(len(new_image_array)):
        for j in range(len(new_image_array[0])):
            if(image_array.ndim == 3):
                for k in range(len(new_image_array[0][0])):
                    new_image_array[i,j,k] = image_array[min(int(round(i / scaley)), len(image_array) - 1), min(int(round(j / scalex)), len(image_array[0]) - 1), k]
            elif(image_array.ndim == 2):
                new_image_array[i,j] = image_array[min(int(round(i / scaley)), len(image_array) - 1), min(int(round(j / scalex)), len(image_array[0]) - 1)]


    return new_image_array