######################################################
##  SihinaCode > Search YouTube for more tutorials  ##
######################################################

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color:rgba(0, 0, 0, 0);\n"
"}\n"
"QWidget#mainWidget{\n"
"    background-color:rgb(12, 11, 16);\n"
"}\n"
"QWidget#titleBar{\n"
"    background-color:rgb(0, 0, 0);\n"
"}\n"
"QWidget#titleBar QLabel#title{\n"
"    color:white;\n"
"    font-size:13px;\n"
"    padding-left:2px;\n"
"}\n"
"QWidget#titleBar QLabel#icon{\n"
"    padding-left:10px;\n"
"      padding-top:4px;\n"
"    padding-right:3px;\n"
"    padding-bottom:4px;\n"
"}\n"
"QWidget#titleBar QPushButton{\n"
"    background-color:rgba(0, 0, 0, 0);\n"
"    color:rgb(255, 255, 255);\n"
"    border-radius:1px;\n"
"}\n"
"QWidget#titleBar QPushButton#closeButton{\n"
"    font-size:12px;\n"
"}\n"
"QWidget#titleBar QPushButton#maximizeButton{\n"
"    font-size:10px;\n"
"}\n"
"QWidget#titleBar QPushButton#minimizeButton{\n"
"    font-size:11px;\n"
"}\n"
"QWidget#titleBar QPushButton:hover{\n"
"    background-color:rgb(49, 48, 53);\n"
"}\n"
"QWidget#titleBar QPushButton#closeButton:hover{\n"
"    background-color:rgb(232, 17, 35);\n"
"}\n"
"QWidget#titleBar QPushButton:pressed{\n"
"    padding-top:2px;\n"
"    padding-left:2px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainWidget = QtWidgets.QWidget(self.centralwidget)
        self.mainWidget.setStyleSheet("")
        self.mainWidget.setObjectName("mainWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleBar = QtWidgets.QWidget(self.mainWidget)
        self.titleBar.setMinimumSize(QtCore.QSize(0, 30))
        self.titleBar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.titleBar.setStyleSheet("")
        self.titleBar.setObjectName("titleBar")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.titleBar)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.icon = MovableLabel(self.titleBar)
        self.icon.setMinimumSize(QtCore.QSize(35, 30))
        self.icon.setMaximumSize(QtCore.QSize(35, 30))
        self.icon.setStyleSheet("")
        self.icon.setText("")
        self.icon.setScaledContents(True)
        self.icon.setObjectName("icon")
        self.horizontalLayout_2.addWidget(self.icon)
        self.title = MovableLabel(self.titleBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        self.title.setMinimumSize(QtCore.QSize(50, 30))
        self.title.setMaximumSize(QtCore.QSize(16777215, 30))
        self.title.setStyleSheet("")
        self.title.setObjectName("title")
        self.horizontalLayout_2.addWidget(self.title)
        self.spacerLabel = MovableLabel(self.titleBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spacerLabel.sizePolicy().hasHeightForWidth())
        self.spacerLabel.setSizePolicy(sizePolicy)
        self.spacerLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.spacerLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.spacerLabel.setText("")
        self.spacerLabel.setObjectName("spacerLabel")
        self.horizontalLayout_2.addWidget(self.spacerLabel)
        self.tbWidget = QtWidgets.QWidget(self.titleBar)
        self.tbWidget.setMinimumSize(QtCore.QSize(0, 30))
        self.tbWidget.setMaximumSize(QtCore.QSize(138, 30))
        self.tbWidget.setStyleSheet("")
        self.tbWidget.setObjectName("tbWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.tbWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.minimizeButton = QtWidgets.QPushButton(self.tbWidget)
        self.minimizeButton.setMinimumSize(QtCore.QSize(46, 30))
        self.minimizeButton.setMaximumSize(QtCore.QSize(46, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setBold(True)
        font.setWeight(75)
        self.minimizeButton.setFont(font)
        self.minimizeButton.setObjectName("minimizeButton")
        self.gridLayout.addWidget(self.minimizeButton, 0, 0, 1, 1)
        self.closeButton = QtWidgets.QPushButton(self.tbWidget)
        self.closeButton.setMinimumSize(QtCore.QSize(46, 30))
        self.closeButton.setMaximumSize(QtCore.QSize(46, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setBold(True)
        font.setWeight(75)
        self.closeButton.setFont(font)
        self.closeButton.setStyleSheet("")
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 0, 2, 1, 1)
        self.maximizeButton = QtWidgets.QPushButton(self.tbWidget)
        self.maximizeButton.setMinimumSize(QtCore.QSize(46, 30))
        self.maximizeButton.setMaximumSize(QtCore.QSize(46, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        self.maximizeButton.setFont(font)
        self.maximizeButton.setStyleSheet("")
        self.maximizeButton.setCheckable(True)
        self.maximizeButton.setObjectName("maximizeButton")
        self.gridLayout.addWidget(self.maximizeButton, 0, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.tbWidget)
        self.verticalLayout.addWidget(self.titleBar)
        self.bodyWidget = QtWidgets.QWidget(self.mainWidget)
        self.bodyWidget.setStyleSheet("")
        self.bodyWidget.setObjectName("bodyWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.bodyWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.bodyWidget)
        self.horizontalLayout.addWidget(self.mainWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "Untitled"))
        self.minimizeButton.setText(_translate("MainWindow", ""))
        self.closeButton.setText(_translate("MainWindow", ""))
        self.maximizeButton.setText(_translate("MainWindow", ""))
from sc_mainwindow.components.movable_label import MovableLabel
