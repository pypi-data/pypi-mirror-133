######################################################
##  SihinaCode > Search YouTube for more tutorials  ##
######################################################

from PyQt5 import QtWidgets, QtCore

class MovableLabel(QtWidgets.QLabel):
    mainWindow = None
    movable = 1
    def __init__(self, parent = None):
        super(MovableLabel, self).__init__(parent = parent)
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.movable == 1:
            self.dragPosition = event.globalPos() - self.mainWindow.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.movable == 1:
            self.mainWindow.move(event.globalPos() - self.dragPosition)
            event.accept()