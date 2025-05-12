import cv2
import numpy as np

def pre_process(image):
    ret2, th2 = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((3,3), np.uint8)

    dilation = cv2.dilate(th2, kernel, iterations=1)

    dilation_median = cv2.medianBlur(dilation, 3)
    
    return dilation_median


def extract_characters(image, width=25, overlap=2, space_between=5, initial_space=10):
    dilation_median = pre_process(image)
    
    if overlap > initial_space:
        raise ValueError('overlap cannot be higher than initial space')
    
    characters = []
    
    ov = overlap
    sb = space_between
    w = width
    isp = initial_space
    
    h = image.shape[0]
    
    x, y = 0,0
    
    for i in range(6):
        if i == 0:
            x+=isp
            
        char = dilation_median[y:h, x - ov : x + w + ov].copy()    
        
        characters.append(cv2.medianBlur(char, 3))
            
        x += w + sb
    
    resized_characters = resize_characters(characters)
    
    return resized_characters

def resize_image(image, size=(32, 52)):
    return cv2.resize(image, size)

def resize_characters(list_characters, size=(32, 52)):
    return [resize_image(img, size) for img in list_characters]