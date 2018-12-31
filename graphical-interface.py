import sys
from Station import Station
from StationsArray import StationsArray
from Equipments import Equipments
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Interface(QTabWidget):
    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)

        self.Stations = StationsArray()
        # self.Stations = set()

        self.InputWindow = QWidget()
        self.OutputWindow = QWidget()

        self.addTab(self.InputWindow, "Input window")
        self.addTab(self.OutputWindow, "Output window")

        self.InputWindowTab()
        self.OutputWindowTab()

    def InputWindowTab(self):

        self.Hbox = QHBoxLayout()
        # ------------------------------------------------------------------------------------------------------------ #
        """ Add station section """
        self.AddStationQGridLayout = QGridLayout()
        self.AddStationQFormLayout = QFormLayout()

        self.AddStationLabel = QLabel("Add station section")
        self.AddStationLabel.setAlignment(Qt.AlignCenter)
        self.AddStationQGridLayout.addWidget(self.AddStationLabel, 0, 1)

        self.StationName = QLineEdit()
        self.AddStationQFormLayout.addRow("Station Name", self.StationName)

        self.StationType = QComboBox()
        self.StationType.addItems(["Analog", "Digital"])
        self.AddStationQFormLayout.addRow("Station Type", self.StationType)

        self.AddStationBtn = QPushButton("Add station")
        self.AddStationBtn.clicked.connect(self.AddStation)

        self.AddStationQGridLayout.addLayout(self.AddStationQFormLayout, 2, 1)
        self.AddStationQGridLayout.addWidget(self.AddStationBtn, 3, 1)
        # ------------------------------------------------------------------------------------------------------------ #
        """ Set neighborhood section """
        self.SetNeighborhoodGridLayout = QGridLayout()
        self.SetNeighborhoodFormLayout = QFormLayout()

        self.SetNeighborLabel = QLabel("Set neighbor")
        self.SetNeighborLabel.setAlignment(Qt.AlignCenter)
        self.SetNeighborhoodGridLayout.addWidget(self.SetNeighborLabel, 1, 1)

        self.SourceStationComboBox = QComboBox()
        # self.SourceStationComboBox.setEditable(True)

        self.TargetStationComboBox = QComboBox()

        self.DistanceLineEdit = QLineEdit()

        self.SetNeighborhoodFormLayout.addRow("Source station", self.SourceStationComboBox)
        self.SetNeighborhoodFormLayout.addRow("Target station", self.TargetStationComboBox)
        self.SetNeighborhoodFormLayout.addRow("Distance", self.DistanceLineEdit)

        self.SetNeighborhoodGridLayout.addLayout(self.SetNeighborhoodFormLayout, 2, 1)

        self.SetNeighborhoodButton = QPushButton("Set neighborhood")
        self.SetNeighborhoodGridLayout.addWidget(self.SetNeighborhoodButton, 3, 1)
        self.SetNeighborhoodButton.clicked.connect(self.SetNeighbor)
        # ------------------------------------------------------------------------------------------------------------ #
        """ Send channels to station section """
        self.SendChannelsGrid = QGridLayout()

        self.SendChannelsSourceLabel = QLabel("Source station")
        self.SendChannelsSourceLabel.setAlignment(Qt.AlignCenter)
        self.SendChannelsSourceCombo = QComboBox()

        self.SendChannelsTargetLabel = QLabel("Target station")
        self.SendChannelsTargetLabel.setAlignment(Qt.AlignCenter)
        self.SendChannelsTargetCombo = QComboBox()

        self.SendChannelsAmountLabel = QLabel("Amount\nof channels")
        self.SendChannelsAmountLabel.setAlignment(Qt.AlignCenter)
        self.SendChannelsAmountLineEdit = QLineEdit()

        self.SendChannelsTypeLabel = QLabel("Type\nof channels")
        self.SendChannelsTypeLabel.setAlignment(Qt.AlignCenter)
        self.SendChannelsTypeCombo = QComboBox()

        self.SendChannelsOkBtn = QPushButton("Set channels")

        self.SendChannelsGrid.addWidget(self.SendChannelsSourceLabel, 1, 1)
        self.SendChannelsGrid.addWidget(self.SendChannelsSourceCombo, 2, 1)
        self.SendChannelsGrid.addWidget(self.SendChannelsTargetLabel, 1, 2)
        self.SendChannelsGrid.addWidget(self.SendChannelsTargetCombo, 2, 2)
        self.SendChannelsGrid.addWidget(self.SendChannelsTypeLabel, 1, 3)
        self.SendChannelsGrid.addWidget(self.SendChannelsTypeCombo, 2, 3)
        self.SendChannelsGrid.addWidget(self.SendChannelsAmountLabel, 1, 4)
        self.SendChannelsGrid.addWidget(self.SendChannelsAmountLineEdit, 2, 4)
        self.SendChannelsGrid.addWidget(self.SendChannelsOkBtn, 2, 5)
        # ------------------------------------------------------------------------------------------------------------ #
        self.Hbox.addLayout(self.AddStationQGridLayout)
        self.Hbox.addStretch()
        self.Hbox.addLayout(self.SetNeighborhoodGridLayout)

        self.VBox = QVBoxLayout()
        self.VBox.addLayout(self.Hbox)
        self.VBox.addLayout(self.SendChannelsGrid)

        self.InputWindow.setLayout(self.VBox)

    def OutputWindowTab(self):
        pass

    def AddStation(self):
        """
            Add a Station to self.Station
            Called by self.AddStationBtn in the method InputWindowTab
        """

        self.Stations + Station(self.StationName.text(), self.StationType.currentText())
        print(self.Stations)
        print("Log: new station added")

        """ Updates data on graphical interface """
        self.StationName.setText('')
        print(self.Stations.ReturnLastItem())
        self.SourceStationComboBox.addItem(self.Stations.ReturnLastItem())
        self.TargetStationComboBox.addItem(self.Stations.ReturnLastItem())

    def SetNeighbor(self):
        """
            Sets neighborhood between two stations
            Called by self.SetNeighborhoodButton in the method InputWindowTab
        """
        source_station = self.Stations.StationFromString(self.SourceStationComboBox.currentText())
        target_station = self.Stations.StationFromString(self.TargetStationComboBox.currentText())
        distance = self.DistanceLineEdit.text()
        source_station.SetNeighbor(target_station, int(distance))
        source_station.ShowStation()

    def

def main():
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()