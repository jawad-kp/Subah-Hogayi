from imutils import face_utils
import argparse
import imutils
import dlib
import cv2 as cv


# Video object
ap = argparse.ArgumentParser() #Argument object
ap.add_argument("-p","--shape-predictor", required = True, help="path to facial landmark predictor")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("Loading facial landmark predictor")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])


vid = cv.VideoCapture(0)
while(True):
	retval, frame = vid.read() #Extracting frame from image
	frame = imutils.resize(frame, width=600)
	GrayFrame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	rects = detector(GrayFrame,0)

	for rect in rects:
		shape = predictor(GrayFrame,rect)
		shape = face_utils.shape_to_np(shape)
		# print(len(shape))

		for x,y in shape[6:12]:
			cv.circle(frame, (x, y), 1, (0, 0, 255), -1)
		cv.imshow("Thopda", frame)





	if cv.waitKey(1) & 0xFF == ord('q'): 
	        break
vid.release()
cv.destroyAllWindows()
