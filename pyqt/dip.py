from PyQt4 import QtGui
from math import sqrt
import cv2
import dlib
import numpy as np
import sys


class Dlib():
    def __init__(self):
        self.PREDICTOR_PATH = "../shape_predictor_68_face_landmarks.dat"
        MOUTH_POINTS = list(range(48,  61))
        self.OVERLAY_POINTS = [MOUTH_POINTS]

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.PREDICTOR_PATH)

    def get_landmarks(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rects = self.detector(img,  0)

        if len(rects) > 1:
            print 'TooManyFaces'
        if len(rects) == 0:
            raise ValueError('Error: NoFaces!!')

        return np.matrix([[p.x,  p.y]
                          for p in self.predictor(img, rects[0]).parts()])

    def get_face_mask(self, img, landmarks):
        for group in self.OVERLAY_POINTS:
            hull = cv2.convexHull(landmarks[group])
            return hull


class openCV():
    def __init__(self, capture, flags):
        self.flags = flags
        self.capture = capture
        self.currentFrame = np.array([])
        self.dlib_obj = Dlib()
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def captureNextFrame(self):
        """
        capture frame and reverse RBG BGR and return opencv image
        """
        ret,  readFrame = self.capture.read()

        if not ret:
            print "Error reading Frame!!"
            sys.exit(0)

        readFrame = self.processFrame(readFrame)
        self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        """     converts frame to format suitable for QtGui            """
        try:
            height, width = self.currentFrame.shape[:2]
            img = QtGui.QImage(self.currentFrame,
                               width,
                               height,
                               QtGui.QImage.Format_RGB888)
            img = QtGui.QPixmap.fromImage(img)
            # self.previousFrame = self.currentFrame
            return img
        except Exception, e:
            print "convertFrame: ", e
            return None

    def processFrame(self, img):
        x1 = 0        # hand_box = [(x1, y1), (x2, y2)]
        y1 = 0
        x2 = 300
        y2 = 400

        x3 = 250      # head_box = [(x3, y3), (x4, y4)]
        y3 = 100
        x4 = 600
        y4 = 500

        x5 = 550    # Button
        x6 = 650
        y5 = 0
        y6 = 50

        img = self.checkButton(img, x5, y5, x6, y6)

        self.flags.isSet_button = False
        if self.flags.isSet_button:
            cv2.rectangle(img, (x3, y3), (x4, y4), (50, 50, 50), 1)

            head_frame = img[y3:y4, x3:x4]
            try:
                img[y3:y4, x3:x4] = self.lipSegment(head_frame)
            except ValueError, e:
                # print 'processFrame: ', e
                self.flags.set_stop()
                pass        # To suppress No face Error

        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 1)
            hand_frame = img[y1:y2, x1:x2]

            try:
                mask, counter, hull, (cx, cy), list_far,\
                        list_end, diff1, diff2, depth = \
                        self.count_fingers(hand_frame)

                self.flags.fingers = counter + 1                # For Control
                if(cv2.contourArea(hull) > 3000) and list_far:
                    cv2.drawContours(hand_frame, [hull], 0, (0, 255, 0), 1)
                    cv2.putText(hand_frame, "Fingers = "+str(counter+1),
                                (10, 250), self.font,  1, (0, 0, 255), 1, 1)
                    for i in range(len(list_far)):
                        cv2.putText(img,
                                    str(diff1[i]) + ", " + str(diff2[i]) +
                                    ", " + str(depth[i]), list_end[i],
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
                        cv2.line(hand_frame, list_end[i], list_far[i],
                                 [255, 255, 255], 1, 8)
                        cv2.circle(hand_frame, list_far[i], 4, [0, 0, 255], 2)
                        cv2.circle(hand_frame, list_end[i], 4, [255, 0, 0], 2)

            except ZeroDivisionError, e:
                print "Count_fingers ZeroDivisionError: ", e
            except UnboundLocalError, e:
                print "Count_fingers UnboundLocalError: ", e

        return img

    def checkButton(self, img, x1, y1, x2, y2):
        btn1 = img[y1:y2, x1:x2]
        btn1 = cv2.cvtColor(btn1, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(btn1, 150, 255, cv2.THRESH_BINARY_INV)
        (_, cnts, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        ci = 0
        max_area = 0

        if cnts:
            for i in range(len(cnts)):
                cnt = cnts[i]
                area = cv2.contourArea(cnt)
                if(area > max_area):
                    max_area = area
                    ci = i
            cnt = cnts[ci]

        else:
            cnt = None
        # cv2.drawContours(btn1, cnt, -1, (0,255,0),1)
        # font = cv2.FONT_HERSHEY_SIMPLEX

        self.flags.isSet_prev = self.flags.isSet_cur
        if cnt is not None:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 1)
            hull = cv2.convexHull(cnt)
            cv2.drawContours(btn1, [hull], 0, (0, 0, 255), 1)
            # cv2.putText(img, "Btn1", (0, 50),  font,  1, (255, 0, 0), 1, 16)

            self.flags.isSet_cur = True
        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), (188, 188, 137), 1)
            self.flags.isSet_cur = False
        # cv2.imshow('Img', img)
        return img

    def lipSegment(self, img):
        # self.t1 = cv2.getTickCount()
        landmarks = self.dlib_obj.get_landmarks(img)
        lipHull = self.dlib_obj.get_face_mask(img,  landmarks)
        cv2.drawContours(img, lipHull, -1, (255, 0, 0), 2)
        (x, y), (MA, ma), angle = cv2.fitEllipse(lipHull)
        a = ma/2
        b = MA/2

        eccentricity = sqrt(pow(a, 2)-pow(b, 2))
        eccentricity = round(eccentricity/a, 2)

        cv2.putText(img, 'E = '+str(round(eccentricity, 3)), (10, 350),
                    self.font, 1, (255, 0, 0), 1)

        if(eccentricity < 0.9):
            cv2.putText(img, 'Cmd = O', (10, 300),  self.font,  1,
                        (0, 0, 255), 1, 16)
            self.flags.set_back()
        else:
            cv2.putText(img, 'Cmd = E', (10, 300),  self.font,  1,
                        (0, 0, 255), 1, 16)
            self.flags.set_fwd()

        if angle < 80:
            self.flags.set_left()
        elif angle > 100:
            self.flags.set_right()
        # self.t2 = cv2.getTickCount()
        # print "Time = ", (self.t2-self.t1)/cv2.getTickFrequency()
        return img

    def count_fingers(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Otsu's thresholding after Gaussian filtering
        img = cv2.GaussianBlur(img, (5, 5), 0)
        ret, mask = cv2.threshold(img, 0, 255,
                                  cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        (_, cnts, _) = cv2.findContours(mask,
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        list_far = []
        list_end = []
        list_diff1 = []
        list_diff2 = []
        list_depth = []
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
                    s, e, f, depth = defects[i, 0]
                    depth = depth / 256
                    # start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    if depth > 30:
                        diff2 = (far[0] - end[0])
                        diff1 = (far[1] - end[1])

                        if diff2 < -10 or diff2 < -25 or far[1] >= (cy+40):
                            cv2.putText(img,
                                        str(diff1) + ", " + str(diff2) +
                                        ", " + str(depth), end,
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (0, 0, 0))
                            cv2.line(img, end, far, (0, 0, 0), 1, 1)
                            cv2.circle(img, far, 4, (0, 0, 120), 1)
                            cv2.circle(img, end, 4, (120, 0, 0), 1)
                            continue
                        else:
                            cv2.putText(img,
                                        str(diff1) + ", " + str(diff2) +
                                        ", " + str(depth), end,
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (255, 255, 255))
                            cv2.line(img, end, far, (255, 255, 255), 2, 8)
                            cv2.circle(img, far, 4, (0, 0, 255), 1)
                            cv2.circle(img, end, 4, (255, 0, 0), 1)
                            list_far.append(far)
                            list_end.append(end)
                            list_diff1.append(diff1)
                            list_diff2.append(diff2)
                            list_depth.append(depth)
                            counter += 1

        cv2.imshow("hand", img)
        cv2.waitKey(1)
        return mask, counter, hull1, (cx, cy), \
            list_far, list_end, list_diff1, list_diff2, list_depth
