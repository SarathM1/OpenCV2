import cv2
import numpy as np
from matplotlib import pyplot as plt

def histogram(img):   
	hist,bins = np.histogram(img.flatten(),256,[0,256])

	cdf = hist.cumsum()
	cdf_normalized = cdf * hist.max()/ cdf.max()

	plt.plot(cdf_normalized, color = 'b')
	plt.hist(img.flatten(),256,[0,256], color = 'r')
	plt.xlim([0,256])
	plt.legend(('cdf','histogram'), loc = 'upper left')
	plt.show()

def count_fingers(hand_frame):
	ret,mask = cv2.threshold(hand_frame,100,255,cv2.THRESH_BINARY_INV)
	res = cv2.bitwise_and(hand_frame,hand_frame,mask=mask)

	(cnts,_)=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

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
				if d<12000:
					continue
									
				if far[1] >= (cy+40):
					continue
				else:
					pass
				
				cv2.circle(hand_frame,far,6,[255,255,255],-1)
				cv2.circle(hand_frame,end,6,[255,0,255],-1)
				cntr +=1
	cv2.imshow('Mask',mask)
	cv2.imshow('Fingers',res)
	cv2.imshow('hand_frame',hand_frame)
	return mask

def main():
	img = cv2.imread('hand_frame.jpg',0)
	
	equ = cv2.equalizeHist(img)
	res = np.hstack((img,equ)) #stacking images side-by-side
	
	#histogram(img)
	#histogram(equ)
	count_fingers(img)
	#cv2.imshow('histogram equalised',res)
	cv2.imwrite('hist.jpg',res)
	cv2.waitKey(0)

if __name__ == '__main__':
	main()