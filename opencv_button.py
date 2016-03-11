import cv2
import numpy as np
import dlib
import imutils
from math import sqrt


cap=cv2.VideoCapture(0)

def disp(img,string,coordinates):
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img,string,coordinates, font, 1,(255,0,0),2,1)


def main():
	while True:
		ret,img=cap.read()
		img = cv2.resize(img,None,fx=1.3,fy=1.2,interpolation = cv2.INTER_LINEAR)
		
		btn1 = img[0:100,250:350]
		btn1 = cv2.cvtColor(btn1,cv2.COLOR_BGR2GRAY)
		ret,mask = cv2.threshold(btn1,150,255,cv2.THRESH_BINARY_INV)
		(cnts,_)=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)	
		
		res = cv2.bitwise_and(btn1,btn1,mask=mask)

		(cnts,_)=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		ci = 0
		max_area = 0
		if cnts:
			for i in range(len(cnts)):
				cnt=cnts[i]
				area = cv2.contourArea(cnt)
				if(area>max_area):
					max_area=area
					ci=i
			cnt = cnts[ci]
		else:
			cnt = None
		#cv2.drawContours(btn1,cnt,-1,(0,255,0),1)
		font = cv2.FONT_HERSHEY_SIMPLEX

		if cnt is not None:
			cv2.rectangle(img,(250,0),(350,100),(0,0,0),2)
			hull = cv2.convexHull(cnt)
			cv2.drawContours(btn1,[hull],0,(0,0,255),2)
			cv2.putText(img,"Btn1",(0,50), font, 1,(255,0,0),2,1)
		else:
			cv2.rectangle(img,(250,0),(350,100),(188,188,137),2)

		cv2.imshow('Img',img)
		#cv2.imshow('btn1',mask)


		if cv2.waitKey(20)&0xff==ord('q'):
			cv2.imwrite('btn1.jpg',btn1)
			cv2.imwrite('mask.jpg',mask)
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()