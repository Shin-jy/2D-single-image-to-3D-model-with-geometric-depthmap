import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
import pdb
import math
from scipy.io import loadmat




sys.setrecursionlimit(100000000)#set recursion limit

#Input = './input/input.jpg'
#name1 = "./output/seg_final.jpg"		#input file 1
#name2 = "./output/sceneGrouping.jpg"		#input file 2


name1 = sys.argv[1]			#input file 1
name2 = sys.argv[2]			#input file 2
img = cv2.imread(name1)  #threshold segmentation       
img1 = cv2.imread(name2) #scene segmentation

 #inintializing
 #1) threshold segmentation to grayscale images
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #cv2.imwrite('img.jpg',gray)
gray0 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
gray1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
gray2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
gray3 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
gray4 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 

 #2) scene segmentation to grayscale images
gray5 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)  

 # Inform the input size 
height, width = gray.shape
print (height, width) #print height and width of image


 # 1-1) Euclidean Depth cue : vanishing point 
xi=int(sys.argv[3])#Vanishing point coordinates
yj=int(sys.argv[4])
max = -1
matrix = [[0 for x in range(width)] for y in range(height)] 
for i in range(0, height):
	for j in range(0, width):
		matrix[i][j] = np.sqrt((i-yj)**2 + (j-xi)**2) + 0.01 #print matrix[i][j]
		if(matrix[i][j]>max):
			max = matrix[i][j]

for i in range(0, height):
	for j in range(0, width):
		gray1[i][j] = (matrix[i][j]*255)/max



			
cv2.imwrite('./output/euclideanDepth.jpg',gray1)




#1-2) (room layout map)  orientation map

omap_r = loadmat('./Layout/omap_r.mat') 
omap_g = loadmat('./Layout/omap_g.mat')
omap_b = loadmat('./Layout/omap_b.mat')
omapArray_r = omap_r['omap_r']
omapArray_g = omap_g['omap_g']
omapArray_b = omap_b['omap_b']

gray_r = gray1 * omapArray_r
gray_g = gray1 * omapArray_g
gray_b = gray1 * omapArray_b

count_r=np.count_nonzero(gray_r )
count_g=np.count_nonzero(gray_g )
count_b=np.count_nonzero(gray_b )

gray_r = omapArray_r*round(gray_r.sum() / count_r) 
gray_g = omapArray_g*round(gray_g.sum() / count_g)
gray_b = omapArray_b*round(gray_b.sum() / count_b)  
gray = gray_r + gray_g + gray_b 

cv2.imwrite('./output/roomLayout.jpg',gray)



 # 1-1&2) combined depth map- vanishing point depth & room layout depth
xi = float(xi)
weightR = xi/(10*height)
print (weightR)
weightH = 1-weightR
for i in range(0, height):
	for j in range(0, width):
		gray2[i][j] = weightR*gray[i][j] + weightH*gray1[i][j]

cv2.imwrite('./output/combinedDepth.jpg',gray2)



 # 1-1&2) Local depth map - combined depthmap & region based segmentation
for i in range(0, height):
	for j in range(0, width):
		gray2f = gray2[i][j].astype('float') #combined Depth cue to float type
		gray3f = gray3[i][j].astype('float') #region based segmentation to grayscale images
		if(gray3f == 0.0):# if region based segmentation is black
                        additionF = gray2f
		else:
			additionF = (gray2f+gray3f)/2 #if threshold segmentation has any color, plus euclidean-depth to any color 
		gray4[i][j] = additionF.astype('uint8') # Local depth map

cv2.imwrite('./output/localDepth.jpg',gray4)



 # 2) final depth map - local depthmap(gray4,gray6) & scene grouping (gray5)

gray6 = gray4  

#scene segmentation의 오픈소스 사용#
def isSafe(i, j, visited):  # function to check if a given cell & (row, col) can be included in DFS
    return (i >= 0 and i < height and j >= 0 and j < width and not visited[i][j]) # row & column is in range and value is 1 and not yet visited

def static_vars(**kwargs):  # for static variable in python
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(var=1)
def DFS(i, j, visited, count, list): #Depth First Search Recursive algorithm
 
        # These arrays are used to get row and column numbers of 8 neighbours of a given cell
        rowNbr = [-1, -1, -1,  0, 0,  1, 1, 1]
        colNbr = [-1,  0,  1, -1, 1, -1, 0, 1]

        list.append([i,j]) 
        DFS.var = 1
        count = count+1
        #print(count)
    
        visited[i][j] = True # Mark this cell as visited
    
        # Recur for all connected neighbours
        for k in range(8): #####error####
            if isSafe(i + rowNbr[k], j + colNbr[k], visited) and gray5[i][j] == gray5[i + rowNbr[k]][j + colNbr[k]] and gray0[i][j]>0:
                DFS(i + rowNbr[k], j + colNbr[k], visited, count,list) #####error: too many recursive####
                
 
        if(DFS.var == 1):
        	sum = 0
        	value = 0
        	for pair in list: # pair means [i,j]
        		sum = sum+gray2[pair[0]][pair[1]]
        		value = value + 1
        	sum = sum/(value+0.05)
        	if sum > 255:
        		for pair in list:
        			print (gray5[pair[0]][pair[1]]+gray2[pair[0]][pair[1]])/2
        		sum = 255
        	for pair in list:
        		grayf = gray5[pair[0]][pair[1]].astype('float')
        		gray2f = gray2[pair[0]][pair[1]].astype('float')
        		additionF = sum
        		gray6[pair[0]][pair[1]] = additionF.astype('uint8')
        	
        DFS.var = 0 		
		


visited = [[False for j in range(width)]for i in range(height)]
for i in range(0, height):
	for j in range(0, width):
		if(gray0[i][j]>0):
			if visited[i][j] == False:
				count = 0
				list = []
				DFS(i, j, visited, count, list)

gray6 = 255*((gray6 - np.min(gray6)) / (np.max(gray6)-np.min(gray6)))
gray6 = gray6.astype('uint8')


cv2.imwrite('./output/depthMap.jpg',gray6)

cv2.waitKey()






