import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
r,h,c,w = 250,90,400,125  # simply hardcoded the values
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
cv2.circle(frame, (c,r), 5, [0, 0, 0], -1)
cv2.circle(frame, (c+w,r+h), 5, [0, 0, 0], -1)

cv2.imshow("ROI",roi)
cv2.imshow("frame",frame)

hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

def count_fingers(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Otsu's thresholding after Gaussian filtering
    img = cv2.GaussianBlur(img, (5, 5), 0)
    ret, mask = cv2.threshold(img, 0, 255,
                              cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow("Threshold", mask)

    (_, cnts, _) = cv2.findContours(mask,
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    list_far = []
    list_end = []
    if cnts:
        areas = [cv2.contourArea(c) for c in cnts]
        max_index = np.argmax(areas)
        cnt = cnts[max_index]

        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        hull1 = cv2.convexHull(cnt)

        hull2 = cv2.convexHull(cnt, returnPoints=False)

        try:
            defects = cv2.convexityDefects(cnt, hull2)
        except Exception,  e:
            defects = None
            print e

        counter = 0
        if defects is not None:
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                # start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                if d < 20000:
                    continue
                if far[1] >= (cy+40):
                    continue

                diff1 = abs(end[0]-far[0])
                if diff1 > 100:
                    continue

                cv2.line(img, end, far, (0, 0, 0), 2, 8)
                cv2.imshow("hand", img)
                cv2.waitKey(1)
                list_far.append(far)
                list_end.append(end)
                counter += 1

    return mask, counter, hull1, (cx, cy), list_far, list_end

while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # Draw it on image
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame,[pts],True, 255,2)
        #[cv2.circle(img2, tuple(p), 5, [0, 0, 0], -1) for p in pts]
        x1,y1 = pts[1]
        x2,y2 = pts[3]
        
        cv2.circle(img2,(x1,y1),5,[0,0,0],-1)
        cv2.circle(img2,(x2,y2),5,[255,0,0],-1)
        
        try:
          cv2.imshow("ROI2",img2[y1:y2,x1:x2])
        except Exception, e:
          print 1

        try:
          cv2.imshow("ROI2",img2[y2:y1,x2:x1])
        except Exception, e:
          print 2
        cv2.imshow('img2',img2)
        #print "\npts = ", pts
        for p in pts:
          print tuple(p)
        #count_fingers(img2)
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            cv2.imwrite(chr(k)+".jpg",img2)
            break

    else:
        break

cv2.destroyAllWindows()
cap.release()