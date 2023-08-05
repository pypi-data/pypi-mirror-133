######################################################
##  SihinaCode > Search YouTube for more tutorials  ##
######################################################

from PyQt5 import QtWidgets
from sc_mainwindow.components.body_ui import Ui_Form

class Body(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Body, self).__init__()
        self.setupUi(self)