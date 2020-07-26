# canny.py by Jiro Mizuno

# Using matplotlib instead of opencv, because I want to implement the steps by myself
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import sys
import math
import os

SIZE = 21

def canny(imgPath):
    img = mpimg.imread(imgPath)
    gray = grayScale(img) # convert to grayscale
    gauss = gaussFilter(gray) # apply a gaussian filter
    plt.axis("off")
    plt.imshow(gauss, cmap='gray')
    plt.show()

# greyscales an matplotlib image by using ITU-R 601-2 luma transformation
# based on https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
def grayScale(img):
    return np.dot(img, [0.2989, 0.5870, 0.1140])

# apply a gaussian filter to the image
# implemented with heavy guidance from:
# https://computergraphics.stackexchange.com/questions/39/how-is-gaussian-blur-implemented
def gaussFilter(img):
    # get the gaussian kernel and convolve it with the image
    return convolve(img, kernel(SIZE, math.sqrt(SIZE)))

# utilize a sobel filter to find grid intensity
def gradIntensity():
    return False

def convolve(img, filterArray):
    # get the dimensions of the image and the kernel
    imgRow, imgCol = img.shape
    fRow, fCol = filterArray.shape

    # create a padded image with a zero-d border for calculating convolution later more easily
    padImg = np.zeros((imgRow+fRow, imgCol+fCol))
    padImg[fRow//2:imgRow+fRow//2, fCol//2:imgCol+fCol//2] = img

    # initialize the result img
    result = np.zeros((imgRow, imgCol))

    # gaussian filter each pixel based on its surroundings
    for i in range(imgRow):
        for j in range(imgCol):
            result[i,j] = np.sum(filterArray * padImg[i:i+fRow, j:j+fCol])

    return result

# creates a gaussian kernel for later use in filtering
def kernel(size, sd):
    k1 = np.zeros(size)
    center = size // 2
    for i in range(size):
        k1[i] = gauss(sd, i-center)
    
    k2 = np.outer(k1,k1)
    print(k2)
    print(np.sum(k2))
    plt.axis("off")
    plt.imshow(k2, cmap='gray')
    plt.show()
    return k2

# calculates the gaussian distribution for both 1d and 2d
def gauss(sd, x, y = 0):
    return 1/math.sqrt(2*math.pi*sd**2) * math.exp(-(x**2 + y**2)/(2*sd**2))

# requires 1 path to the image
if __name__ == '__main__':
    if len(sys.argv) < 3:
        pic = os.getcwd() + "\\" + sys.argv[1]
        canny(pic)
    else:
        print("Function requires only 1 picture")
        raise SystemExit