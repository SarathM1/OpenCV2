import cv2
import numpy as np
cap=cv2.VideoCapture(0)

def disp(string,coordinates):
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame,string,coordinates, font, 1,(255,0,0),2,1)

while True:
	try:
		ret,frame=cap.read()
		frame = cv2.medianBlur(frame,5)    # 5 is a fairly small kernel size
		hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		#lower_blue=np.array([20,40,50])
		#upper_blue=np.array([74,255,255])
		
		lower_blue=np.array([2,11,30])
		upper_blue=np.array([43,90,80])

		mask=cv2.inRange(hsv,lower_blue,upper_blue)
		res = cv2.bitwise_and(frame,frame,mask=mask)
		res_gray=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
		(cnts,_)=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		#print len(cnts)

		# Find the index of the largest contour
		areas = [cv2.contourArea(c) for c in cnts]
		max_index = np.argmax(areas)
		cnt=cnts[max_index]

		# Contour
		#cv2.drawContours(frame, cnt, -1,(0,250,0),2,maxLevel=1)
		
		# Rectangle
		x,y,w,h = cv2.boundingRect(cnt)
		
		aspect_ratio = round(float(w)/h,2)
		rect_area = w*h
		area = cv2.contourArea(cnt)
		extent = round(float(area)/rect_area,2) 
		
		#cv2.circle(frame,(x,y),4,[255,0,0],-1)
		#cv2.circle(frame,(x+w,y+h),4,[255,0,0],-1)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

		# Hull
		hull = cv2.convexHull(cnt)
		cv2.drawContours(frame,[hull],0,(0,0,255),2)
		
		hull_area = cv2.contourArea(hull)
		solidity = round(float(area)/hull_area,2)
		
		(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
		angle = round(angle,2)
		#disp('Angle = '+ str(angle),(10,100)) 				# Orientation
		#disp('Aspect Ratio = '+ str(aspect_ratio),(10,150))	# Rectangle width/height
		#disp('Extent = '+ str(extent),(10,200))				#ratio of contour area to bounding rectangle area.
		#disp('Solidity = '+ str(solidity),(10,250))			# ratio of contour area to its convex hull area.	

		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_gray,mask = mask)

		""" average color of an object. 
		Or it can be average intensity of the object in grayscale mode; 
		x can be ignored"""
		b,g,r,x = cv2.mean(frame,mask = mask)
		#mean_val = cv2.mean(frame,mask = mask)
		bgr = (round(b),round(g),round(r))
		#disp("Mean Val = "+str(bgr),(10,300))

		leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
		rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
		topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
		bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
		#cv2.circle(frame,leftmost,6,[255,0,0],-1)
		#cv2.circle(frame,rightmost,6,[255,0,0],-1)
		#cv2.circle(frame,topmost,6,[255,0,0],-1)
		#cv2.circle(frame,bottommost,6,[255,0,0],-1)
		
		cv2.imshow('mask',mask)
		#cv2.imwrite("blur_frame.jpg",frame)	# Debugging; SLOWWWW operation
		#cv2.imwrite("mask.jpg",mask)			# Debugging; SLOWWWW operation
		
		#cv2.imshow('res',res)
		#cv2.imshow('res_gray',res_gray)
		cv2.imshow('frame',frame)
		
		if cv2.waitKey(20)&0xff==ord('q'):
			break

	except Exception, e:
		print e

cap.release()
cv2.destroyAllWindows()
