

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import matplotlib
import numpy
from PIL import Image
import matplotlib.pyplot as plt
import skimage.io as io

"load image data"

from skimage import color
RGBImage = io.imread('poops.jpg')
ImgGrey = color.rgb2gray(RGBImage)     # Gray image

#thinning algorithm begins
def neighbours(x,y,image):
    "Return 8-neighbours of image point P1(x,y), in a clockwise order"
    img = image
    x_1, y_1, x1, y1 = x-1, y-1, x+1, y+1
    return [ img[x_1][y], img[x_1][y1], img[x][y1], img[x1][y1],     # P2,P3,P4,P5
                img[x1][y], img[x1][y_1], img[x][y_1], img[x_1][y_1] ]    # P6,P7,P8,P9

def transitions(neighbours):
    "No. of 0,1 patterns (transitions from 0 to 1) in the ordered sequence"
    n = neighbours + neighbours[0:1]      # P2, P3, ... , P8, P9, P2
    return sum( (n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]) )  # (P2,P3), (P3,P4), ... , (P8,P9), (P9,P2)

def zhangSuen(image):
    "the Zhang-Suen Thinning Algorithm"
    Image_Thinned = image.copy()  # deepcopy to protect the original image
    changing1 = changing2 = 1        #  the points to be removed (set as 0)
    while changing1 or changing2:   #  iterates until no further changes occur in the image
        # Step 1
        changing1 = []
        rows, columns = Image_Thinned.shape               # x for rows, y for columns
        for x in range(1, rows - 1):                     # No. of  rows
            for y in range(1, columns - 1):            # No. of columns
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, Image_Thinned)
                if (Image_Thinned[x][y] == 1     and    # Condition 0: Point P1 in the object regions 
                    2 <= sum(n) <= 6   and    # Condition 1: 2<= N(P1) <= 6
                    transitions(n) == 1 and    # Condition 2: S(P1)=1  
                    P2 * P4 * P6 == 0  and    # Condition 3   
                    P4 * P6 * P8 == 0):         # Condition 4
                    changing1.append((x,y))
        for x, y in changing1: 
            Image_Thinned[x][y] = 0
        # Step 2
        changing2 = []
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, Image_Thinned)
                if (Image_Thinned[x][y] == 1   and        # Condition 0
                    2 <= sum(n) <= 6  and       # Condition 1
                    transitions(n) == 1 and      # Condition 2
                    P2 * P4 * P8 == 0 and       # Condition 3
                    P2 * P6 * P8 == 0):            # Condition 4
                    changing2.append((x,y))    
        for x, y in changing2: 
            Image_Thinned[x][y] = 0
    return Image_Thinned


#get the red stop cordinate index
def getStopCordinates(RGBimage):
	im=numpy.asarray(RGBimage)

	shape= im.shape
	rows= shape[0]
	cols=shape[1]
	redCordinates=[]

	for i in range(0,rows): 
		for j in range(0,cols):
			if im[i][j][0]in range(170,256) and im[i][j][1] in range(0,50) and im[i][j][2] in range(0,50)  : 
				sys.stdout.write("red : "+ str(im[i][j]) +"("+str(i)+","+str(j)+")" + "\n ")
				redCordinates.append((i,j))
				
	return redCordinates

#get the green cordinate index

def getStartCordinates(RGBimage):
	im=numpy.asarray(RGBimage)

	shape= im.shape
	rows= shape[0]
	cols=shape[1]
	
	greenCordinates=[]

	for y in range(0,rows): 
		for x in range(0,cols):
			if im[y][x][0]in range(0,50) and im[y][x][1] in range(170,256) and im[y][x][2] in range(0,50): 
				sys.stdout.write("green : "+ str(im[y][x]) +"("+str(y)+","+str(x)+")" + "\n ")
				greenCordinates.append((y,x))				
					
	return greenCordinates




def embbedStartAndEndToIntegerMatrix(image): # input ndarray of image or image itself -- output ndarray with start,end
	im=numpy.asarray(image)
	print im.shape
	print len(im)
	print len(im[0])
	imMatrix=[[0 for x in range(len(im[0]))] for y in range(len(im))] 
	
	
	"get stop cordinates"

	stopCordinatesList= getStopCordinates(RGBImage) # return approximate stop cordinate list
	
	"get start cordinates"

	startCordinatesList= getStartCordinates(RGBImage) # return approximate stop cordinate list
	
	

	#to verify the elements which are 1
	for y in range(0,len(im)):
		for x in range(0,len(im[0])):
			if(im[y][x]==1):
				sys.stdout.write("("+str(y)+","+str(x)+")\n")
	
	for x in range(0,len(im)):
		for y in range(0,len(im[0])):
			if(im[x][y]==1):
				imMatrix[x][y]=1
			else:
				imMatrix[x][y]=0
		


	flag=0
	for y1 in range(0,len(startCordinatesList)):
		for x1 in range(0,len(startCordinatesList[0])):
			if(im[startCordinatesList[y1][0]][startCordinatesList[y1][1]]==1):
				print("start marked")
				imMatrix[startCordinatesList[y1][0]][startCordinatesList[y1][1]]=3
				flag=1
				break
		if flag==1:
			break

	flag=0

	for y2 in range(0,len(stopCordinatesList)):
		for x2 in range(0,len(stopCordinatesList[0])):
					#print("moonchi")
			if(im[(stopCordinatesList[y2][0])][stopCordinatesList[y2][1]]==1):
				print("stop marked")
				imMatrix[stopCordinatesList[y2][0]][stopCordinatesList[y2][1]]=9
				flag=1
				break
		if flag==1:
			break
								
	return imMatrix

def printImageUsingSymbols(image):
	#print array as . and #
	im=numpy.asarray(image)
	
	for x in range(0,len(im)):
		for y in range(0,len(im[0])):
			
			if im[x][y] == 3 :
				sys.stdout.write('$')
			elif im[x][y] == 9:
				sys.stdout.write('!')
			else:			
				if(im[x][y]==1):
					sys.stdout.write('@')
				else:
					sys.stdout.write('.')
			
				
		print('\n')
 
def printImageUsingZeorsAndOnes(image):
	im=numpy.asarray(image)
	for x in range(0,len(im)):
		for y in range(0,len(im[0])):
			if(im[x][y]==1):
				sys.stdout.write('1')
			else:
				sys.stdout.write('0')
		print('\n')



"Convert gray images to binary images using Otsu's method"

from skimage.filter import threshold_otsu
Otsu_Threshold = threshold_otsu(ImgGrey)   
BW_Original = ImgGrey < 0.9   # must set object region as 1, background region as 0 !

print( threshold_otsu(ImgGrey))
"Apply the algorithm on images"
BW_Skeleton = zhangSuen(BW_Original)

im=numpy.asarray(BW_Skeleton)


startEndEmbbedMatrix = embbedStartAndEndToIntegerMatrix(BW_Skeleton)
#print(startEndEmbbedMatrix)

print((RGBImage[19][291]))
"printing array"


printImageUsingSymbols(startEndEmbbedMatrix)

" print image-ndarray as zeros and ones "

#printImageUsingZeorsAndOnes(im)










"Display the results"
fig, ax = plt.subplots(1, 2)
ax1, ax2 = ax.ravel()
ax1.imshow(ImgGrey, cmap=plt.cm.gray)
ax1.set_title('Original binary image')
ax1.axis('off')
#print numpy.nonzero(im)
ax2.imshow(BW_Skeleton, cmap=plt.cm.gray)
ax2.set_title('Skeleton of the image')
ax2.axis('off')
plt.show()

