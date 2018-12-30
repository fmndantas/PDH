import sys
from Station import Station
from Equipments import Equipments
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Interface(QTabWidget):
    def __init__(self, parent=None):
        """ Initialization of necessary objects """
        self.Stations = list()

        super(Interface, self).__init__(parent)
        """ Initialization of interface """
        self.QGridLayout = QGridLayout()
        self.QFormLayout = QFormLayout()

        self.StationName = QLineEdit()
        self.QFormLayout.addRow("Station Name", self.StationName)

        self.StationType = QComboBox()
        self.StationType.addItems(["Analog", "Digital"])
        self.QFormLayout.addRow("Station Type", self.StationType)

        self.AddStationBtn = QPushButton("Add station")
        self.AddStationBtn.clicked.connect(self.AddStation)

        self.hSplitter = QSplitter(Qt.Vertical)


        self.QGridLayout.addLayout(self.QFormLayout, 1, 1)
        self.QGridLayout.addWidget(self.AddStationBtn, 2, 1)

        self.setLayout(self.QGridLayout)
        self.setWindowTitle("PDH projector")

    def AddStation(self):
        """ Add a Station to self.Station """
        self.Stations.append(Station(self.StationName.text(), self.StationType.currentText()))
        print("Log: new station added")
        # string = list(map(lambda station : station.ShowStation(), self.Stations))
        # print(string)

    def SetNeighbor(self):
        """ Sets neighborhood """


def main():
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()