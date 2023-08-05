######################################################
##  SihinaCode > Search YouTube for more tutorials  ##
######################################################

from PyQt5 import QtWidgets, QtCore, QtGui
from sc_mainwindow.components.main_window_ui import Ui_MainWindow
from sc_mainwindow.components.movable_label import MovableLabel
from sc_mainwindow.components.resizable_mwindow import ResizableMainWindow
from sc_mainwindow.components.body import Body
import sc_mainwindow.components.sihinaRes_rc
import sys

class MainWindow(ResizableMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.fontDB = QtGui.QFontDatabase()
        self.fontDB.addApplicationFont(":/sihinaFonts/segmdl2.ttf")
        self.setupUi(self)
        MovableLabel.mainWindow = self
        self.grip_size = 8
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=12, xOffset=0, yOffset=0, color=QtGui.QColor(0, 0, 0, 255))
        self.centralwidget.setGraphicsEffect(self.shadow)
        self.minimizeButton.clicked.connect(self.winShowMinimized)
        self.maximizeButton.clicked.connect(self.winShowMaximized)
        self.closeButton.clicked.connect(sys.exit)
        self.body = Body()
        self.verticalLayout_2.addWidget(self.body)
        self.setIcon(":/sihinaImages/sihinaLogo.png")

        
    def winShowMinimized(self):
        self.showMinimized()

    def winShowMaximized(self):
        if self.maximizeButton.isChecked():
            self.setGripSize(0)
            self.showMaximized()
            MovableLabel.movable = 0
            self.maximizeButton.setText("")    
        else:
            self.setGripSize(self.grip_size)
            self.showNormal()
            MovableLabel.movable = 1
            self.maximizeButton.setText("")

    def insertBody(self, widget):
        self.body.hide()
        self.verticalLayout_2.addWidget(widget)
        
    def setTitleBarColor(self, r=0, g=0, b=0, a=255):
        self.titleBar.setStyleSheet("QWidget#titleBar{background-color:rgba(%s, %s, %s, %s);}"%(r, g, b, a))

    def setIcon(self, image:str):
        pixmap = QtGui.QPixmap(image)
        self.icon.setPixmap(pixmap)

    def setTransparent(self, val:float=1 ):
        self.setWindowOpacity(val)

    def setFrameShadow(self, enable:bool):
        self.shadow.setEnabled(enable)

    def setShadowColor(self, r=0, g=0, b=0, a=255, blurRadius=12):
        self.shadow.setColor(QtGui.QColor(r, g, b, a))
        self.shadow.setBlurRadius(blurRadius)

    def setTitleText(self, text:str):
        self.title.setText(text)

    def setBorderColor(self, r=0, g=0, b=0, a=255):
        self.mainWidget.setStyleSheet("QWidget#mainWidget{border:1px solid rgba(%s, %s, %s, %s);}"%(r, g, b, a))

    def fixFlickeringWindow(self, val=1):
        self.grip_size = val
        self.setGripSize(self.grip_size)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)

def runExample():
        app = QtWidgets.QApplication(sys.argv)
        Form = MainWindow()
        Form.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        Form = MainWindow()
        Form.show()
        sys.exit(app.exec_())
