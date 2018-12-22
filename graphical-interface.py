import sys
from Station import Station
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Interface(QTabWidget):
    def __init__(self, parent=None):
        """ Initialization of necessary objects """
        self.Station = list()

        super(Interface, self).__init__(parent)
        """ Initialization of interface """
        self.MainLayout = QGridLayout()
        self.AddStationBtn = QPushButton("Add station")
        self.MainLayout.addWidget(self.AddStationBtn, 1, 1)
        self.setLayout(self.MainLayout)

    def AddStation(self):
        """ Add a Station to self.Station """

def main():
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()