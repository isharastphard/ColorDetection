import cv2
import numpy as np
import argparse 
import pandas as pd

#creating the image parser so image can be loaded from cmd line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = "Image Path" )
args = vars(ap.parse_args())
img_path = args['image']
 #reading the image with opencv
img = cv2.imread(img_path)

#global variables to be used later on
clicked = False
r = g = b = xpos = ypos = 0

#reading csv file with pandas and naming each column something easy
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names = index, header = None)

#function to calculate minimum distance from all colors and pick the color the matches most
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#draw_function checks if the event is double clicked and sets the r,g,b values of the spot double clicked to x,y positions of the mouse
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while(1):
    cv2.imshow("image", img)
    if(clicked):
        #cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle entirely <------- arguments for the cv2.rectangle function
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
        #Creating text string to display ( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)
        #cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) ) <------- arguments for cv2.putText function
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
  #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked=False
    #Break the loop when user hits 'esc' key 
    if cv2.waitKey(20) & 0xFF ==27:
        break
cv2.destroyAllWindows()







