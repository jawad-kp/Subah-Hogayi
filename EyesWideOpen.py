from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import dlib
import cv2 as cv
import numpy as np

def eye2eye(eye):

	# Vertical eye landmarks
	# print(eye)
	# print(len(eye))
	A = dist.euclidean(eye[1],eye[5])
	B = dist.euclidean(eye[2],eye[4])

	#Horizontal eye landmarks
	C = dist.euclidean(eye[0],eye[3])

	EasR = (A+B)/(2.0 *C)
	return EasR

# Video object
ap = argparse.ArgumentParser() #Argument object
ap.add_argument("-p","--shape-predictor", required = True, help="path to facial landmark predictor")
args = vars(ap.parse_args())

EyeThres = 0.2
ConsFrame = 5

counter,blinks = 0,0

print("Loading shit in... ")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(lStart, lEnd) = (0,6)
(rStart, rEnd) = (6,12)

# vid = cv.VideoCapture(0)
vs = VideoStream(src=0).start()
while(True):
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	# detect faces in the grayscale frame
	# leftEye,rightEye = [],[]
	rects = detector(gray, 0)
	for rect in rects:
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye2eye(leftEye)
		rightEAR = eye2eye(rightEye)
		# average the eye aspect ratio together for both eyes
		ear = (leftEAR + rightEAR) / 2.0
		leftEyeHull = cv.convexHull(leftEye)
		rightEyeHull = cv.convexHull(rightEye)
		cv.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		leftEyeHull = cv.convexHull(leftEye)
		rightEyeHull = cv.convexHull(rightEye)
		cv.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		if ear < EyeThres:
			blinks += 1
		# otherwise, the eye aspect ratio is not below the blink
		# threshold
		else:
			# if the eyes were closed for a sufficient number of
			# then increment the total number of blinks
			if counter >= ConsFrame:
				counter += 1
			# reset the eye frame counter
			counter = 0
		cv.putText(frame, "Blinks: {}".format(blinks), (10, 30),
		cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
		cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	cv.imshow("Thopda With Blinks", frame)
	key = cv.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
cv.destroyAllWindows()
vs.stop()




	