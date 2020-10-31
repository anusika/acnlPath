from PIL import ImageGrab
import cv2
import numpy as np
import win32gui

def windowCallback(hwnd, hwndFound, name="Snickerstream"):

    if name in win32gui.GetWindowText(hwnd):
        hwndFound.append(hwnd)
    return True

def getWindow():
    hwndFound = []
    win32gui.EnumWindows(windowCallback, hwndFound)
    return win32gui.GetWindowRect(hwndFound[0])


windowSize = getWindow()
print(windowSize)
halfheight = (windowSize[3] - windowSize[1])/2
bottomScreen = (windowSize[0], windowSize[1] + halfheight, windowSize[2], windowSize[3])
topScreen = (windowSize[0], windowSize[1], windowSize[2], windowSize[3] - halfheight)

while True:
    screen = np.array(ImageGrab.grab(windowSize, all_screens=True))
    RGB_img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

    height, width, channels = RGB_img.shape

    bottomImg = RGB_img[round((height/2)):height, 0:width]

    lower = np.array([0, 0, 200])
    upper = np.array([0, 0, 255])
    shapeMask = cv2.inRange(bottomImg, lower, upper)

    white_pixels = np.array(np.where(shapeMask == 255))
    
    if white_pixels.size == 0:
        first_white_pixel = (0, 0)
    else:
        first_white_pixel = white_pixels[:,0] 
        first_white_pixel = (first_white_pixel[1], first_white_pixel[0])

    print(first_white_pixel)
    #center = (first_white_pixel[0], first_white_pixel(1))

    radius = 10

    color = (0, 255, 0)

    thickness = 2

    image = cv2.circle(bottomImg, first_white_pixel, radius, color, thickness)
    

    cv2.imshow('Python Window', image)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
