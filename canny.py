# canny.py by Jiro Mizuno

# Using matplotlib instead of opencv, because I want to implement the steps by myself
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import sys
import math
import os

SIZE = 5
HIGH = 0.2
LOW = 0.2

def canny(imgPath):
    img = mpimg.imread(imgPath)
    gray = grayScale(img) # convert to grayscale
    gauss = gaussFilter(gray) # apply a gaussian filter
    grad, dir = gradIntensity(gauss) # apply a sorbel filter and get gradient directions
    nonMax = nonMaxSuppression(grad, dir) # suppress the non maximum gradients
    doubleT = doubleThreshold(nonMax)
    cannied = edgeTrack(doubleT)
    plt.axis("off")
    plt.imshow(cannied, cmap='gray')
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

# utilizes a sobel filter to find grid intensity
# implementation based on https://en.wikipedia.org/wiki/Sobel_operator 
def gradIntensity(img):
    # get the x and y kernals
    xKernal = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    yKernal = np.array([[1, 2, 1], [0, 0, 0], [-1,-2,-1]])

    # get convolved x and y images
    Gx = convolve(img, xKernal)
    Gy = convolve(img, yKernal)

    # get the hypotenuse to find the intensity of the gradient
    G = np.hypot(Gx,Gy)

    # readjust pixel levels to the 0-255 scale for visibility
    G = G/np.max(G) * 255

    # get the arctan to find the direction of the gradient
    theta = np.arctan2(Gy,Gx)
    return G, theta

# suppresses all non maximum gradients
def nonMaxSuppression(img, dir):
    imgRow, imgCol = img.shape
    result = np.zeros(img.shape)

    for i in range(imgRow):
        for j in range(imgCol):
            # figure out the closest axis and set the directional neighbors

            # West-East
            if (-math.pi/8 < dir[i,j] <= math.pi/8) or (7*math.pi/8 < dir[i,j]) or (dir[i,j] <= -7*math.pi/8):
                l = img[i, max(0, j-1)]
                r = img[i, min(imgCol-1, j+1)]
            
            # Northwest-Southeast
            elif (math.pi/8 < dir[i,j] <= 3*math.pi/8) or (-7*math.pi/8 < dir[i,j] <= -5*math.pi/8):
                l = img[max(0, i-1), max(0, j-1)]
                r = img[min(imgRow-1, i+1), min(imgCol-1, j+1)]

            # North-South
            elif (3*math.pi/8 < dir[i,j] <= 5*math.pi/8) or (-5*math.pi/8 < dir[i,j] <= -3*math.pi/8):
                l = img[max(0, i-1), j]
                r = img[min(imgRow-1, i+1), j]
            
            # Southwest - Northeast
            else:
                l = img[min(imgRow-1, i+1), max(0, j-1)]
                r = img[max(0, i-1), min(imgCol-1, j+1)]
            
            # if the current pixel is greater than its directional neighbors, keep it
            # otherwise, zero it out
            if l <= img[i,j] and r <= img[i,j]:
                result[i,j] = img[i,j]

    return result

# separate non-revelant and relevant pixels and then separate the relevant to strong and weak
# implemented with guidance from http://justin-liang.com/tutorials/canny/#double-thresholding
def doubleThreshold(img, low = LOW, high = HIGH):
    # set the high and low thresholds
    highT = np.max(img) * high
    lowT = highT * low

    imgRow, imgCol = img.shape

    # change non-revelant to black, weak to grey, strong to white
    for i in range(imgRow):
        for j in range(imgCol):
            if img[i,j] < lowT:
                img[i,j] = 0
            elif img[i,j] < highT:
                img[i,j] = 60
            else:
                img[i,j] = 255
    
    return img

# change all weak pixels that are next to strong pixels to strong and discard the rest
# implemented with help from https://en.wikipedia.org/wiki/Canny_edge_detector 
def edgeTrack(img):
    imgRow, imgCol = img.shape

    for i in range(imgRow):
        for j in range(imgCol):
            if img[i,j] == 60:
                if ((img[i, max(0, j-1)] == 255) or (img[i, min(imgCol-1, j+1)] == 255)
                or (img[max(0, i-1), max(0, j-1)] == 255) or (img[min(imgRow-1, i+1), min(imgCol-1, j+1)] == 255)
                or (img[max(0, i-1), j] == 255) or (img[min(imgRow-1, i+1), j] == 255)
                or (img[min(imgRow-1, i+1), max(0, j-1)] == 255) or (img[max(0, i-1), min(imgCol-1, j+1)] == 255)):
                    img[i,j] = 255
                else:
                    img[i,j] = 0
    return img

def convolve(img, filterArray):
    # get the dimensions of the image and the kernel
    imgRow, imgCol = img.shape
    fRow, fCol = filterArray.shape

    # create a padded image with a zero-d border for calculating convolution later more easily
    padImg = np.zeros((imgRow+fRow, imgCol+fCol))
    padImg[fRow//2:imgRow+fRow//2, fCol//2:imgCol+fCol//2] = img

    # color in the padding pixels with the "generally closest" pixel colors so
    # the borders don't get darkened when convolving at the edge
    padImg[:fRow//2, :fCol//2] = img[0,0]
    padImg[:fRow//2, imgCol+fCol//2:] = img[0,imgCol-1]
    padImg[imgRow+fRow//2:,imgCol+fCol//2:] = img[imgRow-1,imgCol-1]
    padImg[imgRow+fRow//2:, :fCol//2] = img[imgRow-1,0]

    for i in range(imgRow):
        padImg[fRow//2 + i, :fCol//2] = img[i,0]
        padImg[fRow//2 + i, imgCol+fCol//2:] = img[i, imgCol-1]
    for i in range(imgCol):
        padImg[:fRow//2, i + fCol//2] = img[0, i]
        padImg[imgRow+fRow//2:, i + fCol//2] = img[imgRow-1, i]

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