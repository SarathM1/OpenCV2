import cv2
import numpy as np

cap=cv2.VideoCapture(0)

def disp(string,coordinates):
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(btn1,string,coordinates, font, 1,(255,0,0),2,1)

def count_fingers(cnts,btn1):
	if cnts:
		areas = [cv2.contourArea(c) for c in cnts]
		max_index = np.argmax(areas)
		cnt=cnts[max_index]

		M = cv2.moments(cnt)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		cv2.circle(img,(cx,cy),6,[59,53,255],-1)

		hull = cv2.convexHull(cnt)
		cv2.drawContours(img,[hull],0,(0,0,255),2)

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
				if d<12000:
					continue
				
				if far[1] >= (cy+40):
					continue
				else:
					pass
					#print far[1],cy
				#dist = cv2.pointPolygonTest(cnt,far,True)
				cv2.circle(img,far,6,[100,100,0],-1)
				cv2.circle(img,end,6,[255,0,255],-1)
				cntr +=1

		disp("No of finger's = "+str(cntr+1),(10,300))


while True:
	ret,img=cap.read()
	img = cv2.medianBlur(img,3)    # 5 is a fairly small kernel size
	cv2.rectangle(img,(0,0),(300,300),(50,200,0),3)
	btn1 = img[0:300,0:300]

	hsv_btn1 = cv2.cvtColor(btn1,cv2.COLOR_BGR2HSV)
	lower_skin = np.array([0,7,30])
	upper_skin = np.array([150,90,120])
	mask = cv2.inRange(hsv_btn1,lower_skin,upper_skin)
	res = cv2.bitwise_and(btn1,btn1,mask=mask)

	(cnts,_)=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	
	try:
		count_fingers(cnts,btn1)
	except Exception, e:
		print e
	
	
	#cv2.imwrite('btn1.jpg', btn1)
	#cv2.imwrite('mask.jpg', mask)
	cv2.imshow('mask',mask)
	cv2.imshow('Res',res)
	cv2.imshow('Img',img)
	
	if cv2.waitKey(20)&0xff==ord('q'):
		break

cap.release()
cv2.destroyAllWindows()