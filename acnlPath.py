from PIL import ImageGrab
import cv2
import numpy as np
import win32gui
import itertools
import random
import argparse


#contains all coordiantes for path
path = []
#name of tool/window for streaming from 3ds
name = "Snickerstream"

def windowCallback(hwnd, hwndFound, name = name):
    """
    callback function for getWindow
    check if hwnd found matches 3ds streaming window
    """
    if name in win32gui.GetWindowText(hwnd):
        hwndFound.append(hwnd)
    return True

def getWindow():
    """
    get window size of 3ds streaming window
    """
    hwndFound = []
    win32gui.EnumWindows(windowCallback, hwndFound)
    return win32gui.GetWindowRect(hwndFound[0])


def getPoints():

    windowSize = getWindow()

    while True:
        #get image of window and convert to RGB
        screen = np.array(ImageGrab.grab(windowSize, all_screens=True))
        RGB_img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        #get height and width of window to select bottom screen of 3ds
        height, width, channels = RGB_img.shape
        bottomImg = RGB_img[round((height/2)):height, 0:width]

        #create a mask that picks only the red pixels in a image
        #this is because the location of your character is in a red shape
        lower = np.array([0, 0, 200])
        upper = np.array([0, 0, 255])
        shapeMask = cv2.inRange(bottomImg, lower, upper)

        #check for the first white pixel in the mask that represents your location
        #if a white pixel can't be found add a placeholder of (0, 0)
        whitePixels = np.array(np.where(shapeMask == 255))

        if whitePixels.size == 0:
            center = (0, 0)
        else:
            center = whitePixels[:,0] 
            center = (center[1], center[0])

        #add white pixel location to path
        path.append(center)

        #add a green circle of your current location on the image
        radius = 10
        color = (0, 255, 0)
        thickness = 2
        image = cv2.circle(bottomImg, center, radius, color, thickness)


        cv2.imshow('Python Window', image)

        #if 'q' is pressed end the sampling
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return image
            break

def createPathImage(image):
    """
    creates a red path line based on cooridates in path list
    """
    #remove consecutive duplicates to reduce drawing time
    #remove placeholder (0,0)
    global path
    path = [corr for corr, _ in itertools.groupby(path)]
    path = [corr for corr in path if corr != (0 , 0)]
    #draw coordinate as a red circle
    for corr in path:
        cv2.drawMarker(image, (corr[0], corr[1]),(0,0,255), markerType=cv2.MARKER_CROSS, 
        markerSize=2, thickness=2, line_type=cv2.LINE_AA)
    cv2.imshow('Python Window', image)
    cv2.waitKey()
    return image


def saveImg(image):
    number = str(random.randint(1111,9999))
    filename = "ACNL" + number + ".jpg"
    cv2.imwrite(filename, image)


def main():
    #pick a different streaming client besides SnickerStream
    parser = argparse.ArgumentParser(description='Create a Path :)')
    parser.add_argument('--stream', dest='stream', action='store', default=False,
                    help='name of streaming window')
    args = parser.parse_args()
    if args.stream:
        global name
        name = args.stream

    #first get the path
    image = getPoints()
    #create path drawing
    image = createPathImage(image)
    #save image as .jpeg
    saveImg(image)


if __name__ == "__main__":
    main()