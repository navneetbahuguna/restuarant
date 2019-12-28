'''from django.shortcuts import render
import numpy as np 
import urllib 
import json
import cv2
import os

from django.http import JsonResponse

faceDetector = 'haarcascade_frontalface_default.xml'

def read_image(path=None, stream=None, url=None):

    ##### primarily URL but if the path is None
    ## load the image from your local repository

    if path is not None:
        image = cv2.imread(path)

    else:
        if url is not None:

            response = urllib.request.urlopen(url)

            data_temp = response.read()

        elif stream is not None:
            #implying image is now streaming
            data_temp = stream.read()

        image = np.asarray(bytearray(data_temp), dtype="uint8")

        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image

def requested_url(request):
    #default value set to be false

    default = {"safely executed": False} #because no detection yet

    ## between GET or POST, we go with Post request and check for https

    if request.method == "POST":
        if request.FILES.get("image", None) is not None:

            image_to_read = read_image(stream = request.FILES["image"])


        else: # URL is provided by the user
            url_provided = request.POST.get("url", None)


            if url_provided is None:
                default["error_value"] = "There is no URL Provided"

                return JsonResponse(default)

            image_to_read = read_image(url = url_provided)


        image_to_read = cv2.cvtColor(image_to_read, cv2.COLOR_BGR2GRAY)

        detector_value = cv2.CascadeClassifier(face_detector)
            #passing the face detector path
            # make sure to pass the complete path to the .xml file


        values = detector_value.detectMultiScale(image_to_read,
                                                 scaleFactor=1.1,
                                                 minNeighbors = 5,
                                                 minSize=(30,30),
                                                 flags = cv2.CASCADE_SCALE_IMAGE)

        ###dimensions for boxes that will pop up around the face
        values=[(int(a), int(b), int(a+c), int(b+d)) for (a,b,c,d) in values]

        default.update({"#of_faces": len(values),
                        "faces":values,
                        "safely_executed": True })

    return JsonResponse(default)

'''

import numpy as np
import imutils
import cv2
 
class SingleMotionDetector:
	def __init__(self, accumWeight=0.5):
		# store the accumulated weight factor
		self.accumWeight = accumWeight
 
		# initialize the background model
		self.bg = None

    def update(self, image):
		# if the background model is None, initialize it
		if self.bg is None:
			self.bg = image.copy().astype("float")
			return
 
		# update the background model by accumulating the weighted
		# average
		cv2.accumulateWeighted(image, self.bg, self.accumWeight)
    def detect(self, image, tVal=25):
		# compute the absolute difference between the background model
		# and the image passed in, then threshold the delta image
		delta = cv2.absdiff(self.bg.astype("uint8"), image)
		thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
 
		# perform a series of erosions and dilations to remove small
		# blobs
		thresh = cv2.erode(thresh, None, iterations=2)
		thresh = cv2.dilate(thresh, None, iterations=2)
        # find contours in the thresholded image and initialize the
		# minimum and maximum bounding box regions for motion
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		(minX, minY) = (np.inf, np.inf)
		(maxX, maxY) = (-np.inf, -np.inf)
        # if no contours were found, return None
		if len(cnts) == 0:
			return None
 
		# otherwise, loop over the contours
		for c in cnts:
			# compute the bounding box of the contour and use it to
			# update the minimum and maximum bounding box regions
			(x, y, w, h) = cv2.boundingRect(c)
			(minX, minY) = (min(minX, x), min(minY, y))
			(maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))
 
		# otherwise, return a tuple of the thresholded image along
		# with bounding box
		return (thresh, (minX, minY, maxX, maxY))
