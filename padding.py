#Import Libraries
import numpy as np

#Zero padding
def zero_padding(image_array,size):
    pad_amount = int(size/2)
    if(image_array.ndim == 3):
        return np.pad(image_array,pad_width=((pad_amount,pad_amount),(pad_amount,pad_amount),(0,0)),mode='constant', constant_values=0)
    elif(image_array.ndim == 2):
        return np.pad(image_array,pad_width=((pad_amount,pad_amount),(pad_amount,pad_amount)),mode='constant', constant_values=0)