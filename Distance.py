from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import glob
import csv
import math
from matplotlib import pyplot as plt


detected = False


#Parameters

#width of reference object in Inches
#Quarter's are 1.29in
width = 1.114

#Week of trial data
Week = 13

#photos location
datapictures = 'C:/Users/Hunter/PycharmProjects/CheckerDistance/Week 12.2/*.JPG'


#Location of Calibration Object compared to Origin in Inches.
CalibrationX = 3.0
CalbirationY = 0


#Determine whether a picture will show or not.

graypicture = False # shows gray image of picture
edgedpicture = False #shows image of contours
finalpicture = False # output image




def midpoint(ptA,ptB):
    return  ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)



#create two arrays for location of calibration dots. Calibration dots are in order (Bottom Left, Top Left, Bottom Right, Top Right)

files = []
for filename in glob.glob(datapictures):
    files.append(filename)



ReferenceX = ['Reference X']
CheckerX = ['Checker X']
ReferenceY = ['Reference Y']
CheckerY = ['Checker Y']
Ratio = ['Ratio (pixel/in)']
DxP = ['Difference in X (Pixel)']
DyP = ['Difference in Y (Pixel)']
Dxin =['Location X (In)']
Dyin = ['Location Y (In)']
counters = ['Amount of Measurements']



points = []
for x in range(0,len(files)):
    imagefile = files[x]

    # determines how many contours found
    counter = 0



    # load the image, convert it to grayscale, and blur it slightly
    image = cv2.imread(imagefile,0)
    gray = image

    if graypicture == True:
        plt.imshow(gray,cmap='gray')
        plt.show()



    gray = cv2.GaussianBlur(gray, (7, 7), 0)



    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 15, 80)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)


    if edgedpicture == True:
        plt.imshow(edged,cmap='gray')
        plt.show()

    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]




    # sort the contours from left-to-right and, then initialize the
    # distance colors and reference object
    (cnts, _) = contours.sort_contours(cnts)
    colors = ((0, 0, 255), (240, 0, 159), (9, 92, 148), (176, 31, 9),
        (255, 0, 255))
    refObj = None

    # loop over the contours individually
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 10000:

            continue
        # compute the rotated bounding box of the contour
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        box = perspective.order_points(box)

        # compute the center of the bounding box
        cX = np.average(box[:, 0])
        cY = np.average(box[:, 1])







        # if this is the first contour we are examining (i.e.,
        # the left-most contour), we presume this is the
        # reference object
        if refObj is None:
            # unpack the ordered bounding box, then compute the
            # midpoint between the top-left and top-right points,
            # followed by the midpoint between the top-right and
            # bottom-right
            (tl, tr, br, bl) = box
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)

            # compute the Euclidean distance between the midpoints,
            # then construct the reference object
            D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            refObj = (box, (cX, cY), D / width)
            ratio = D/width
            reference = [c]

            continue

        # draw the contours on the image
        image = cv2.imread(imagefile)


        orig = image.copy()
        cv2.drawContours(orig, [box.astype("int")], -1, (255, 0, 0), 2)
        cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
        # stack the reference coordinates and the object coordinates
        # to include the object center
        refCoords = np.vstack([refObj[0], refObj[1]])
        objCoords = np.vstack([box, (cX, cY)])

        # loop over the original points

        #top for loops shows the box edges where the last only shows center
        #for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
        refCoords = refCoords[-1]
        objCoords = objCoords[-1]
        ((xA, yA), (xB, yB), color) = (refCoords, objCoords, colors[-1])

        # draw circles corresponding to the current points and
        # connect them with a line
        cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
        cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
        cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
                 color, 2)
        cv2.drawContours(orig, [c], -1, (0, 0, 255), 2)
        cv2.drawContours(orig, reference, -1, (255, 0, 0), 2)

        # compute the Euclidean distance between the coordinates,
        # and then convert the distance in pixels to distance in
        # units
        D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]

        (mX, mY) = midpoint((xA, yA), (xB, yB))
        cv2.putText(orig, "{:.3f}in".format(D), (int(mX), int(mY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 5, color, 2)

        counter = counter + 1
        #puts all the information into lists
        #NOTE: All numbers are references of distance of Checker to Reference. The only numbers that are values of Checker to Origin are Dxin and Dyin.
        ReferenceX.append(xA)
        CheckerX.append(xB)
        ReferenceY.append(yA)
        CheckerY.append(yB)
        Ratio.append(round(ratio,4))
        DxP.append(xA-xB)
        DyP.append(yB-yA)

        Dxin.append(np.round(CalibrationX + (xA - xB)/ratio ,4))
        Dyin.append(np.round(CalbirationY + (yB-yA)/ratio,4))
        counters.append(counter)
        detected = True

        # show the output image

        if finalpicture == True:
            plt.imshow(orig,)
            plt.show()



    #determines if program detected distance. If it didnt throw out the name of the file
    if detected == False:
        print(str(imagefile) +' could not detect either the reference or checker.')
        ReferenceX.append("NA")
        CheckerX.append("NA")
        ReferenceY.append("NA")
        CheckerY.append("NA")
        Ratio.append("NA")
        DxP.append("NA")
        DyP.append("NA")

        Dxin.append("NA")
        Dyin.append("NA")
        counters.append('NA')
    else:
        detected = False


#send data to csv file
with open('Week '+ str(Week) +' Trial Runs.csv','w',newline ='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter =',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    for x in range(0,len(ReferenceX)):
        holder = (ReferenceX[x],CheckerX[x],ReferenceY[x],CheckerY[x],Ratio[x],DxP[x],DyP[x],Dxin[x],Dyin[x],counters[x])
        filewriter.writerow(holder)