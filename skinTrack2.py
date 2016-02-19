import cv2
import numpy as np

cap=cv2.VideoCapture(0)

def disp(img,string,coordinates):
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img,string,coordinates, font, 1,(255,0,0),2,1)

def count_fingers(cnts,hand_frame,img):
	if cnts:
		areas = [cv2.contourArea(c) for c in cnts]
		max_index = np.argmax(areas)
		cnt=cnts[max_index]

		M = cv2.moments(cnt)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		cv2.circle(hand_frame,(cx,cy),6,[59,53,255],-1)

		hull = cv2.convexHull(cnt)
		cv2.drawContours(hand_frame,[hull],0,(0,0,255),2)

		hull = cv2.convexHull(cnt,returnPoints = False)
		
		try:
			defects = cv2.convexityDefects(cnt,hull)
		except Exception, e:
			defects = None
			print e

		cntr = 0
		if defects is not None:
			for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				start = tuple(cnt[s][0])
				end = tuple(cnt[e][0])
				far = tuple(cnt[f][0])
				if d<12400:
					continue
									
				if far[1] >= (cy+40):
					continue
				else:
					pass
				
				cv2.circle(hand_frame,far,6,[100,100,0],-1)
				cv2.circle(hand_frame,end,6,[255,0,255],-1)
				cntr +=1

		disp(hand_frame,"Fingers = "+str(cntr+1),(10,230))

def main():
	while True:
		ret,img=cap.read()
		img = cv2.medianBlur(img,3)    # 5 is a fairly small kernel size
		cv2.rectangle(img,(0,150),(250,400),(50,50,50),2)
		#cv2.rectangle(img,(400,0),(700,400),(0,255,0),3)
		
		hand_frame = img[150:400,0:250]

		hsv_btn1 = cv2.cvtColor(hand_frame,cv2.COLOR_BGR2HSV)
		lower_skin = np.array([0,7,30])
		upper_skin = np.array([150,90,120])
		mask = cv2.inRange(hsv_btn1,lower_skin,upper_skin)
		res = cv2.bitwise_and(hand_frame,hand_frame,mask=mask)

		(cnts,_)=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		
		try:
			count_fingers(cnts,hand_frame,img)
		except ZeroDivisionError, e:
			print "Count_fingers: ",e
		
		
		#cv2.imwrite('hand_frame.jpg', hand_frame)
		#cv2.imwrite('mask.jpg', mask)
		cv2.imshow('mask',mask)
		cv2.imshow('Res',res)
		cv2.imshow('Img',img)
		
		if cv2.waitKey(20)&0xff==ord('q'):
			cv2.imwrite('hand_frame.jpg', hand_frame)
			cv2.imwrite('mask.jpg', mask)
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()