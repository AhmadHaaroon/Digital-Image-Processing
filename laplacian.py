#Import Libraries
import numpy as np

#Import files
from input import input_text
import convolution
import padding as pad

#Gaussian filter
def gaussian_filter(image_array, sigma=None, size=None, padding=None):