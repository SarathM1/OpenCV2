# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created: Fri Mar 11 15:19:06 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    latch_button_state = False
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1076, 664)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.videoFrame = QtGui.QLabel(self.centralwidget)
        self.videoFrame.setGeometry(QtCore.QRect(160, 10, 891, 601))
        self.videoFrame.setText(_fromUtf8(""))
        self.videoFrame.setObjectName(_fromUtf8("videoFrame"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 140, 141, 171))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.up_arrow = QtGui.QToolButton(self.gridLayoutWidget)
        self.up_arrow.setEnabled(False)
        self.up_arrow.setText(_fromUtf8(""))
        self.up_arrow.setArrowType(QtCore.Qt.UpArrow)
        self.up_arrow.setObjectName(_fromUtf8("up_arrow"))
        self.gridLayout.addWidget(self.up_arrow, 0, 1, 1, 1)
        self.left_arrow = QtGui.QToolButton(self.gridLayoutWidget)
        self.left_arrow.setEnabled(False)
        self.left_arrow.setText(_fromUtf8(""))
        self.left_arrow.setArrowType(QtCore.Qt.LeftArrow)
        self.left_arrow.setObjectName(_fromUtf8("left_arrow"))
        self.gridLayout.addWidget(self.left_arrow, 2, 0, 1, 1)
        self.down_arrow = QtGui.QToolButton(self.gridLayoutWidget)
        self.down_arrow.setEnabled(False)
        self.down_arrow.setText(_fromUtf8(""))
        self.down_arrow.setArrowType(QtCore.Qt.DownArrow)
        self.down_arrow.setObjectName(_fromUtf8("down_arrow"))
        self.gridLayout.addWidget(self.down_arrow, 1, 1, 1, 1)
        self.right_arrow = QtGui.QToolButton(self.gridLayoutWidget)
        self.right_arrow.setEnabled(False)
        self.right_arrow.setText(_fromUtf8(""))
        self.right_arrow.setArrowType(QtCore.Qt.RightArrow)
        self.right_arrow.setObjectName(_fromUtf8("right_arrow"))
        self.gridLayout.addWidget(self.right_arrow, 2, 1, 1, 1)
        self.stop = QtGui.QPushButton(self.gridLayoutWidget)
        self.stop.setStyleSheet(_fromUtf8("background-color :rgb(190, 56, 56) ;"))
        self.stop.setObjectName(_fromUtf8("stop"))
        self.gridLayout.addWidget(self.stop, 0, 0, 1, 1)
        self.latch = QtGui.QPushButton(self.gridLayoutWidget)
        self.latch.setStyleSheet(_fromUtf8("background-color :rgb(190, 56, 56) ; ;\n"
""))
        self.latch.setObjectName(_fromUtf8("latch"))
        self.gridLayout.addWidget(self.latch, 1, 0, 1, 1)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 120, 161, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(0, 310, 161, 20))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.line_5 = QtGui.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(-3, 440, 161, 20))
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 330, 141, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label.setEnabled(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 390, 141, 51))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setEnabled(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.mode = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.mode.setStyleSheet(_fromUtf8("background-color :rgb(190, 56, 56) ; ;\n"
""))
        self.mode.setObjectName(_fromUtf8("mode"))
        self.horizontalLayout_3.addWidget(self.mode)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1076, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "OpenCV", None))
        self.stop.setText(_translate("MainWindow", "Off", None))
        self.latch.setText(_translate("MainWindow", "Latch", None))
        self.label.setText(_translate("MainWindow", "Fingers", None))
        self.label_2.setText(_translate("MainWindow", "Mode", None))
        self.mode.setText(_translate("MainWindow", "Relay", None))

