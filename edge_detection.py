#Import Libraries
from PIL import Image
import cv2
import numpy as np
import queue

#Import Files
import gaussian
import sobel
import convolution
import padding as pad
from input import input_text

#Enhancement Function
def edge_detection(image_array):
    new_image_array=None

    #Check enhancement method
    option = input_text("Which edge detection method do you wish to perform?:\n1)Marr–Hildreth Edge Detection" \
                    "\n2)Canny Edge Detection\n\nOption Selected:",2)

    if(option==1):
        new_image_array=marr_hildreth_edge(image_array,0.15,'Zero')

    elif(option==2):
        high_threshold = -1
        low_threshold = -1
        while(high_threshold<0 or high_threshold>100):
            try:
                high_threshold = float(input("Enter a high threshold value (in %): "))
                if(high_threshold<0 or high_threshold>100):
                    print("\nInvalid option entered, please try again.\n")
                else:
                    print()
                    selected=True
            except:
                print("\nInvalid option entered, please try again.\n")

        while(low_threshold<0 or low_threshold>100):
            try:
                low_threshold = float(input("Enter a low threshold value (in %): "))
                if(low_threshold<0 or low_threshold>100):
                    print("\nInvalid option entered, please try again.\n")
                else:
                    print()
                    selected=True
            except:
                print("\nInvalid option entered, please try again.\n")
                
        new_image_array=canny_edge(image_array,high_threshold,low_threshold,'Zero')

    return new_image_array


#Marr-Hildreth Edge Detection
def marr_hildreth_edge(image_array,threshold=None,padding=None):
    #Create new arrays
    if(image_array.ndim == 3):
        gaussian_result = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0])))
        laplacian_result = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0])))
        new_image_array = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0])))
    elif(image_array.ndim == 2):
        gaussian_result = np.zeros((len(image_array),len(image_array[0])))
        laplacian_result = np.zeros((len(image_array),len(image_array[0])))
        new_image_array = np.zeros((len(image_array),len(image_array[0])))

    #Step 2: Applying laplacian filter
    laplacian_matrix = np.array([[0,1,0],[1,-4,1],[0,1,0]])
    gaussian_matrix = gaussian.gaussian_matrix_calculation(1.4,5)
    hybrid_matrix = np.zeros((len(laplacian_matrix),len(laplacian_matrix[0])))

    hybrid_matrix = convolution.convolution(gaussian_matrix,hybrid_matrix,laplacian_matrix)
    hybrid_matrix = hybrid_matrix - (np.ones((len(hybrid_matrix),len(hybrid_matrix[0]))) * np.mean(hybrid_matrix))

    #Select padding type, if none set
    if(padding==None):
        option = input_text("Select padding type:\n1)Zero Padding\n\nOption Selected:",1)
        if(option == 1):
            image_array = pad.zero_padding(image_array,3)
    else:
        #Padding image
        image_array = pad.zero_padding(image_array,3)

    laplacian_result = convolution.convolution(image_array,new_image_array,hybrid_matrix)

    #Step 3: Finding zero crossings
    #Select padding type, if none set
    if(padding==None):
        option = input_text("Select padding type:\n1)Zero Padding\n\nOption Selected:",1)
        if(option == 1):
            laplacian_result = pad.zero_padding(laplacian_result,3)
    else:
        #Padding image
        laplacian_result = pad.zero_padding(laplacian_result,3)

    if(threshold==None):
        threshold=0
    else:
        threshold = threshold * np.max(laplacian_result)

    for i in range(1,len(laplacian_result)-1):
        l=i-1
        for j in range(1,len(laplacian_result[0])-1):
            m=j-1
            if(np.abs(laplacian_result[i-1][j] - laplacian_result[i+1][j])>threshold):
                if((laplacian_result[i-1][j]>0 and laplacian_result[i+1][j]<0) or
                   (laplacian_result[i-1][j]<0 and laplacian_result[i+1][j]>0)):
                    new_image_array[l][m]=255
                else:
                    new_image_array[l][m]=0

            elif(np.abs(laplacian_result[i][j-1] - laplacian_result[i][j+1])>threshold):
                if((laplacian_result[i][j-1]>0 and laplacian_result[i][j+1]<0) or
                   (laplacian_result[i][j-1]<0 and laplacian_result[i][j+1]>0)):
                    new_image_array[l][m]=255
                else:
                    new_image_array[l][m]=0

            elif(np.abs(laplacian_result[i-1][j-1] - laplacian_result[i+1][j+1])>threshold):
                if((laplacian_result[i-1][j-1]>0 and laplacian_result[i+1][j+1]<0) or
                   (laplacian_result[i-1][j-1]<0 and laplacian_result[i+1][j+1]>0)):
                    new_image_array[l][m]=255
                else:
                    new_image_array[l][m]=0

            elif(np.abs(laplacian_result[i-1][j] - laplacian_result[i+1][j])>threshold):
                if((laplacian_result[i+1][j-1]>0 and laplacian_result[i-1][j+1]<0) or
                   (laplacian_result[i+1][j-1]<0 and laplacian_result[i+1][j+1]>0)):
                    new_image_array[l][m]=255
                else:
                    new_image_array[l][m]=0

            else:
                new_image_array[l][m]=0

    return new_image_array


#Canny Edge Detection
def canny_edge(image_array, high_threshold=90, low_threshold=30, padding=None):
    #Create new arrays
    if(image_array.ndim == 3):
        gaussian_result = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0])))
        thinning_result = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0])))
        new_image_array = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0])))
    elif(image_array.ndim == 2):
        gaussian_result = np.zeros((len(image_array),len(image_array[0])))
        thinning_result = np.zeros((len(image_array),len(image_array[0])))
        new_image_array = np.zeros((len(image_array),len(image_array[0])))

    #Step 1: Apply gaussian filter
    gaussian_result = gaussian.gaussian_filter(image_array,1.4,5,'Zero') #array, sigma, size, padding

    #Step 2: Gradient calculation
    Gx = sobel.sobel_filter(gaussian_result,'Horizontal',padding)
    Gy = sobel.sobel_filter(gaussian_result,'Vertical',padding)

    gradient_magnitude = (np.sqrt(Gx**2 + Gy**2))
    gradient_magnitude = gradient_magnitude / np.max(gradient_magnitude) * 255

    gradient_angle = np.arctan2(Gy,Gx) * 180/np.pi
    gradient_angle[gradient_angle<0] += 180

    #Step 3: Edge thinning via Non-Maximum Suppression
    #Select padding type, if none set
    if(padding==None):
        option = input_text("Select padding type:\n1)Zero Padding\n\nOption Selected:",1)
        if(option == 1):
            gradient_magnitude = pad.zero_padding(gradient_magnitude,3)
    else:
        #Padding image
        gradient_magnitude = pad.zero_padding(gradient_magnitude,3)

    #Check magnitudes along angles
    for i in range(1,len(gradient_magnitude)-1):
        l=i-1
        for j in range(1,len(gradient_magnitude[0])-1):
            m=j-1
            if(image_array.ndim == 3):
                for k in range(len(gradient_magnitude[0][0])):
                    angle = gradient_angle[l][m][k]
                    gradient_values=np.array([
                            gradient_magnitude[i-1][j-1][k], gradient_magnitude[i-1][j][k], gradient_magnitude[i-1][j+1][k],
                            gradient_magnitude[i][j-1][k],   gradient_magnitude[i][j][k],   gradient_magnitude[i][j+1][k],
                            gradient_magnitude[i+1][j-1][k], gradient_magnitude[i+1][j][k], gradient_magnitude[i+1][j+1][k]
                        ])
                    thinning_result[i-1][j-1] = magnitude_check(gradient_values,angle)
            elif(image_array.ndim == 2):
                angle = gradient_angle[l][m]
                gradient_values=np.array([
                        gradient_magnitude[i-1][j-1], gradient_magnitude[i-1][j], gradient_magnitude[i-1][j+1],
                        gradient_magnitude[i][j-1],   gradient_magnitude[i][j],   gradient_magnitude[i][j+1],
                        gradient_magnitude[i+1][j-1], gradient_magnitude[i+1][j], gradient_magnitude[i+1][j+1]
                    ])
                thinning_result[i-1][j-1] = magnitude_check(gradient_values,angle)

    #Step 4: Hysteresis Thresholding and Connectivity Analysis
    #Select padding type, if none set
    if(padding==None):
        option = input_text("Select padding type:\n1)Zero Padding\n\nOption Selected:",1)
        if(option == 1):
            thinning_result = pad.zero_padding(thinning_result,3)
    else:
        thinning_result= pad.zero_padding(thinning_result,3)
    
    #Double threshold analysis (marking strong, weak and irrelevant edges)
    weak = queue.Queue()
    for i in range(1,len(thinning_result)-1):
        for j in range(1,len(thinning_result[0])-1):
            if(image_array.ndim == 3):
                for k in range(len(thinning_result[0][0])):
                    if(thinning_result[i][j][k]>=high_threshold):
                        new_image_array[i-1][j-1][k] = 255
                    elif(thinning_result[i][j][k]<=low_threshold):
                        new_image_array[i-1][j-1][k] = 0
                    elif(thinning_result[i-1][j-1][k] >= high_threshold or
                         thinning_result[i-1][j][k] >= high_threshold or
                         thinning_result[i-1][j+1][k] >= high_threshold or
                         thinning_result[i][j-1][k] >= high_threshold or
                         thinning_result[i][j+1][k] >= high_threshold or
                         thinning_result[i+1][j+1][k] >= high_threshold or
                         thinning_result[i+1][j][k] >= high_threshold or
                         thinning_result[i+1][j+1][k] >= high_threshold):
                        new_image_array[i-1][j-1][k] = 255
                        thinning_result[i][j][k]=255
                    else:
                        new_image_array[i-1][j-1][k] = 0
                        weak.put([i,j,k])

            elif(image_array.ndim == 2):
                if(thinning_result[i][j]>=high_threshold):
                    new_image_array[i-1][j-1] = 255
                elif(thinning_result[i][j]<=low_threshold):
                    new_image_array[i-1][j-1] = 0
                elif(thinning_result[i-1][j-1] >= high_threshold or
                     thinning_result[i-1][j] >= high_threshold or
                     thinning_result[i-1][j+1] >= high_threshold or
                     thinning_result[i][j-1] >= high_threshold or
                     thinning_result[i][j+1] >= high_threshold or
                     thinning_result[i+1][j+1] >= high_threshold or
                     thinning_result[i+1][j] >= high_threshold or
                     thinning_result[i+1][j+1] >= high_threshold):
                   new_image_array[i-1][j-1] = 255
                   thinning_result[i][j]=255
                else:
                    new_image_array[i-1][j-1] = 0
                    weak.put([i,j])

    #Finalizing changes to weak edges
    changed=True
    while(changed==True):
        changed=False
        size=weak.qsize()
        for _ in range(size):
            if(image_array.ndim == 3):
                i,j,k = weak.get()

                if(thinning_result[i-1][j-1][k] >= high_threshold or
                thinning_result[i-1][j][k] >= high_threshold or
                thinning_result[i-1][j+1][k] >= high_threshold or
                thinning_result[i][j-1][k] >= high_threshold or
                thinning_result[i][j+1][k] >= high_threshold or
                thinning_result[i+1][j+1][k] >= high_threshold or
                thinning_result[i+1][j][k] >= high_threshold or
                thinning_result[i+1][j+1][k] >= high_threshold):
                    new_image_array[i-1][j-1][k] = 255
                    thinning_result[i][j][k]=255
                    changed=True
                else:
                    weak.put([i,j,k])

            elif(image_array.ndim == 2):
                i,j = weak.get()

                if(thinning_result[i-1][j-1] >= high_threshold or
                thinning_result[i-1][j] >= high_threshold or
                thinning_result[i-1][j+1] >= high_threshold or
                thinning_result[i][j-1] >= high_threshold or
                thinning_result[i][j+1] >= high_threshold or
                thinning_result[i+1][j+1] >= high_threshold or
                thinning_result[i+1][j] >= high_threshold or
                thinning_result[i+1][j+1] >= high_threshold):
                    new_image_array[i-1][j-1] = 255
                    thinning_result[i][j]=255
                    changed=True
                else:
                    weak.put([i,j])

    
    return new_image_array
    
#Magnitude checking
def magnitude_check(gradient_values, gradient_angle):
    neighbour = None
    if (0 <= gradient_angle < 22.5) or (157.5 <= gradient_angle <= 180):
        neighbour = max(gradient_values[1], gradient_values[7])
    elif (22.5 <= gradient_angle < 67.5):
        neighbour = max(gradient_values[0], gradient_values[8])
    elif (67.5 <= gradient_angle < 112.5):
        neighbour = max(gradient_values[3], gradient_values[5])
    elif (112.5 <= gradient_angle < 157.5):
        neighbour = max(gradient_values[2], gradient_values[6])

    if (gradient_values[4] >= neighbour):
        return gradient_values[4]
    else:
        return 0

#Neighbour checking
def neighbour_checking(hysteresis_array,high_threshold,i,j,k=None):
    if(k==None):
        value = max(hysteresis_array[i][j],
                    hysteresis_array[i][j+1],
                    hysteresis_array[i][j+2],
                    hysteresis_array[i+1][j],
                    hysteresis_array[i+1][j+2],
                    hysteresis_array[i+2][j],
                    hysteresis_array[i+2][j+1],
                    hysteresis_array[i+2][j+2])
        if(value>high_threshold):
            return 255,True
        return -1,False
    else:
        value = max(hysteresis_array[i][j][k],
                    hysteresis_array[i][j+1][k],
                    hysteresis_array[i][j+2][k],
                    hysteresis_array[i+1][j][k],
                    hysteresis_array[i+1][j+2][k],
                    hysteresis_array[i+2][j][k],
                    hysteresis_array[i+2][j+1][k],
                    hysteresis_array[i+2][j+2][k])
        if(value>high_threshold):
            return 255,True
        return -1,False