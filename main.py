#Import libraries
from PIL import Image
import numpy as np
import os

#Import Files
import resize
import enhancement
import edge_detection
from input import input_text

#Clear terminal
while(True):
    _ = os.system('clear')

    #Open Test Image
    try:
        image = Image.open('Test_Image.jpg')
        image = image.convert("L")
        image_array = np.array(image, dtype=np.float32)
    except FileNotFoundError:
        print("Error: 'Test_Image.jpg' not found. Please provide an image file.")
        exit()

    #Select Option
    option = input_text("Which operation do you wish to perform?:\n1)Resize\n2)Enhancement\n3)Edge Detection\n\n" \
            "Option Selected:",3)

    #Option 1: Resize
    if(option==1):
        new_image_array = resize.resize(image_array)
    elif(option==2):
        new_image_array = enhancement.enhancement(image_array)
    elif(option==3):
        new_image_array = edge_detection.edge_detection(image_array)

    output_img = Image.fromarray(new_image_array.astype(np.uint8))
    output_img.save('Result_Image.jpg')
    output_img.show()

    """
    output_img = Image.fromarray(new_image_array.astype(np.uint8))
    output_img.save('Result_Image.jpg')
    output_img.show()
    """