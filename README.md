# edgedetection
A beginner project to practice edge detection technology

# Canny Method

## Overview
Apparently its one of the most used forms of edge detection and it seems relatively straightforward so I'm going to try it out. It also results in very clear edges, so that's helpful. 

Why it's used according to wikipedia:
1. Detects edges with low error rate. (Detects as many edges as can be found)
2. Edge detected is located where edge is.
3. Edge detected once is not detected twice (image noise doesn not create any false edges) 

The amount of data appears to be minimized compared to other forms of edge detection so I will utilize this in preparation of other computer vision projects that require a degree of edge detection. 

## Conceptual Design
Very oversimplified goal:
1. Grey scale the picture
2. Identify parts of the picture where the pixel value changes drastically in shade

More in detail blueprint:
1. Grey scale the image
2. Reduce the noise.
3. Calculate the gradients
4. Suppress non-maximum gradients (making the edges thin)
5. Identifying strong, weak and non-relevant pixels
6. Converting weak pixels to strong if there is a strong pixel around it. (edge tracking by hysteresis)

## Technical Design
Library to use:
- Matplotlib

Blueprint but techincal:
1. Use ITU-R 601-2 luma transformation
2. Implement gaussian filter from scratch
3. 

## Technical Implementation


