import cv2
import numpy as np
import dlib
import imutils
from math import sqrt

cap=cv2.VideoCapture(0)

class Dlib():
	def __init__(self):
		self.PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
		MOUTH_POINTS = list(range(48, 61))
		self.OVERLAY_POINTS = [MOUTH_POINTS]

		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor(self.PREDICTOR_PATH)
	
	def get_landmarks(self,img):
	    rects = self.detector(img, 0)
	    
	    if len(rects) > 1:
	        print 'TooManyFaces'
	    if len(rects) == 0:
	    	raise ValueError('Error: NoFaces!!')
	    	#print "NoFaces"

	    return np.matrix([[p.x, p.y] for p in self.predictor(img, rects[0]).parts()])


	def get_face_mask(self,img,landmarks):
	    for group in self.OVERLAY_POINTS:
	        hull = cv2.convexHull(landmarks[group])
	        cv2.fillConvexPoly(img, hull, 0)


def disp(img,string,coordinates):
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img,string,coordinates, font, 1,(255,0,0),2,1)

def lipSegment(img):
	#img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img = imutils.resize(img,width=300)
	img_copy = img.copy()

	landmarks = dlib_obj.get_landmarks(img)

	dlib_obj.get_face_mask(img_copy, landmarks)
	output_img = img-img_copy
	
	output_img = cv2.cvtColor(output_img,cv2.COLOR_BGR2GRAY)
	contours,hierarchy = cv2.findContours(output_img.copy(), cv2.cv.CV_RETR_EXTERNAL, cv2.cv.CV_CHAIN_APPROX_SIMPLE)  #cv2.findContours(image, mode, method
	cv2.drawContours(img, contours, -1, (0,255,0), 2,maxLevel=0)
	cnt = contours[0]
	ellipse = cv2.fitEllipse(cnt)
	(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
	#cv2.ellipse(img,ellipse,(0,255,0),2)

	
	a = ma/2
	b = MA/2


	eccentricity = sqrt(pow(a,2)-pow(b,2))
	eccentricity = round(eccentricity/a,2)

	font = cv2.FONT_HERSHEY_SIMPLEX

	#cv2.putText(img,'ma = '+str(round(ma,2)),(10,300), font, 1,(255,0,0),2,16)
	#cv2.putText(img,'MA = '+str(round(MA,2)),(10,350), font, 1,(255,0,0),2,16)
	cv2.putText(img,'Eccentr= '+str(round(eccentricity,3)),(10,350), font, 1,(255,0,0),2,16)
	
	if(eccentricity < 0.9):
		cv2.putText(img,'Commands = O',(10,300), font, 1,(0,0,255),2,16)
	else:
		cv2.putText(img,'Commands = E',(10,300), font, 1,(0,0,255),2,16)

	#cv2.imshow('Mask',img_copy)
	#cv2.imshow('Output', output_img)
	return img

def count_fingers(hand_frame):
	hand_frame = cv2.cvtColor(hand_frame,cv2.COLOR_BGR2GRAY) # To avoid error
	ret,mask = cv2.threshold(hand_frame,155,255,cv2.THRESH_BINARY_INV)
	
	(cnts,_)=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	list_far=[]
	list_end=[]
	if cnts:
		areas = [cv2.contourArea(c) for c in cnts]
		max_index = np.argmax(areas)
		cnt=cnts[max_index]

		M = cv2.moments(cnt)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		#cv2.circle(mask,(cx,cy),6,[0,0,0],-1)

		hull1 = cv2.convexHull(cnt)
		#cv2.drawContours(mask,[hull],0,(255,255,255),2)

		hull2 = cv2.convexHull(cnt,returnPoints = False)
		
		try:
			defects = cv2.convexityDefects(cnt,hull2)
		except Exception, e:
			defects = None
			print e

		counter = 0
		if defects is not None:
			for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				start = tuple(cnt[s][0])
				end = tuple(cnt[e][0])
				far = tuple(cnt[f][0])
				if d<20000:
					continue
									
				if far[1] >= (cy+40):
					continue
				else:
					pass
				
				#cv2.circle(mask,far,6,[0,0,0],-1)
				#cv2.circle(mask,end,6,[0,0,0],-1)
				list_far.append(far)
				list_end.append(end)
				counter +=1
		
		#cv2.imshow('hand_frame',mask)
	return mask,counter,hull1,(cx,cy),list_far,list_end

def main():
	while True:
		ret,img=cap.read()
		#img = cv2.medianBlur(img,3)    # 5 is a fairly small kernel size
		img = cv2.resize(img,None,fx=1.3,fy=1.2,interpolation = cv2.INTER_LINEAR)
		cv2.rectangle(img,(0,50),(400,400),(255,255,255),2)
		cv2.rectangle(img,(500,100),(800,500),(50,50,50),2)
		
		head_frame = img[100:500,500:800]
		#head_frame = img.copy()

		try:
			img[100:500,500:800] = lipSegment(head_frame)	
		except ValueError, e:
			#print e
			pass
		hand_frame = img[50:400,0:400]
		
		try:
			mask,counter,hull,(cx,cy),list_far,list_end = count_fingers(hand_frame)
			cv2.drawContours(hand_frame,[hull],0,(0,255,0),1)
			[cv2.circle(hand_frame,far,5,[0,0,0],-1) for far in list_far]
			[cv2.circle(hand_frame,end,5,[255,255,255],-1) for end in list_end]

			if(cv2.contourArea(hull)>0):
				cv2.putText(img[50:400,0:400],"Fingers = "+str(counter+1),(10,250),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,1)
		except ZeroDivisionError, e:
			print "Count_fingers ZeroDivisionError: ",e
		except UnboundLocalError,e:
			print "Count_fingers UnboundLocalError: ",e

		
		
		#cv2.imshow('mask',mask)
		#cv2.imshow('Res',res)
		cv2.imshow('Img',img)
		#cv2.imshow('head_frame',head_frame)
		
		if cv2.waitKey(20)&0xff==ord('q'):
			cv2.imwrite('output.jpg',img)
			cv2.imwrite('hand_frame.jpg', hand_frame)
			cv2.imwrite('mask.jpg', mask)
			cv2.imwrite('head_frame.jpg', head_frame)
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	dlib_obj = Dlib()
	main()
