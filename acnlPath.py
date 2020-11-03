from PIL import ImageGrab
import cv2
import numpy as np
import win32gui
import itertools

path = []

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

def main():
    while True:
        screen = np.array(ImageGrab.grab(windowSize, all_screens=True))
        RGB_img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        height, width, channels = RGB_img.shape

        bottomImg = RGB_img[round((height/2)):height, 0:width]

        lower = np.array([0, 0, 200])
        upper = np.array([0, 0, 255])
        shapeMask = cv2.inRange(bottomImg, lower, upper)

        whitePixels = np.array(np.where(shapeMask == 255))

        if whitePixels.size == 0:
            center = (0, 0)
        else:
            center = whitePixels[:,0] 
            center = (center[1], center[0])

        print(center)
        path.append(center)

        radius = 10
        color = (0, 255, 0)
        thickness = 2
        image = cv2.circle(bottomImg, center, radius, color, thickness)


        cv2.imshow('Python Window', image)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return image
            break




image = main()

path = [corr for corr, _ in itertools.groupby(path)]
path = [corr for corr in path if corr != (0 , 0)]
print(path)

for corr in path:
    cv2.drawMarker(image, (corr[0], corr[1]),(0,0,255), markerType=cv2.MARKER_CROSS, 
    markerSize=2, thickness=2, line_type=cv2.LINE_AA)
cv2.imshow('Python Window', image)
cv2.waitKey(0) 