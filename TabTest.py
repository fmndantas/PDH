import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
from time import sleep


class Interface(QTabWidget):
    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)

        # Flag for first update
        self.firstUpdateFlag = False

        # Letters
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J']

        # Operation frequency of transceptors in KHz and amount of centrals
        self.FreqOp = 15000  # in MHz
        self.AmountOfCentrals = 2

        # Matrix for distances, channels and LP's
        self.nxn = 2
        self.DistMatrix = np.zeros((self.nxn, self.nxn))
        self.ChannelsMatrix = np.zeros_like(self.DistMatrix)
        self.CppMatrix = np.zeros_like(self.DistMatrix)
        self.LPsMatrix = np.empty((self.nxn, self.nxn))

        # Initializes graph for path finding and power array
        self.Graph = []
        self.Prx = []

        # Default prices
        self.PCMPrice = 5000
        self.DoubleSalt = 8000
        self.RadioPrice = 80000
        self.AnthennaPrice = 5000
        self.ModemPrice = 4000
        self.FiberPrice = 15000

        # Tab try
        self.InputWindow = QWidget()
        self.OutputWindow = QWidget()

        self.addTab(self.InputWindow, "Tab 1")
        self.addTab(self.OutputWindow, "Tab 2")

        self.InputWindowTab()
        self.OutputWindowTab()

    def InputWindowTab(self):

        self.layout = QGridLayout()

        self.freqOpLabel = QLabel('Operational frequency \nfor transceptors (MHz):')
        self.layout.addWidget(self.freqOpLabel, 1, 1)

        self.freqOpBox = QLineEdit(str(self.FreqOp))
        self.freqOpBox.setValidator(QIntValidator())
        self.layout.addWidget(self.freqOpBox, 2, 1)

        self.amountCentralsLabel = QLabel('Quantity of stations:')
        self.layout.addWidget(self.amountCentralsLabel, 3, 1)

        # Min: 2, Max: 9
        self.amountCentralsSpinBox = QSpinBox()
        self.amountCentralsSpinBox.setMaximum(9)
        self.amountCentralsSpinBox.setMinimum(2)
        self.layout.addWidget(self.amountCentralsSpinBox, 4, 1)

        self.btnOk = QPushButton('Update properties')
        self.btnOk.setCheckable(True)
        self.btnOk.clicked.connect(self.UpdateValues)
        self.layout.addWidget(self.btnOk, 5, 1)

        self.DistMatrixBtn = QPushButton('Distance Matrix')
        self.DistMatrixBtn.clicked.connect(self.ShowDistMatrix)
        self.layout.addWidget(self.DistMatrixBtn, 2, 2)

        self.ChannelsAndLpsMatrixBtn = QPushButton('Channels and LP\'s\nmatrix')
        self.ChannelsAndLpsMatrixBtn.clicked.connect(self.ShowChannelsMatrix)
        self.layout.addWidget(self.ChannelsAndLpsMatrixBtn, 3, 2)

        self.PricesBtn = QPushButton('Prices table')
        self.PricesBtn.clicked.connect(self.PricesTableDialog)
        self.layout.addWidget(self.PricesBtn, 4, 2)

        self.UpdateLabel = QLabel('')
        self.layout.addWidget(self.UpdateLabel, 6, 1)

        self.setTabText(0, "Input window")
        self.InputWindow.setLayout(self.layout)
        self.setWindowTitle("Input window")

    def OutputWindowTab(self):

        self.layoutOut = QGridLayout()

        self.ChannelsPerPathBtn = QPushButton('Channels per path')
        self.ChannelsPerPathBtn.clicked.connect(self.ChannelsPerPath)  # Process and return the Cpp matrix
        self.ChannelsPerPathBtn.clicked.connect(self.ShowCppMatrix)  # Shows the Cpp matrix
        self.layoutOut.addWidget(self.ChannelsPerPathBtn, 2, 1)

        self.OForRadioBtn = QPushButton('Transmission medium')
        self.OForRadioBtn.clicked.connect(self.OForRadio)
        self.layoutOut.addWidget(self.OForRadioBtn, 3, 1)

        self.setTabText(1, "Output window")
        self.OutputWindow.setLayout(self.layoutOut)

    def PricesTableDialog(self):
        self.PricesDialog = QDialog()
        self.PricesDialog.setWindowTitle("Channels matrix")

        self.flo = QFormLayout()

        self.PCM_le = QLineEdit()
        self.PCM_le.setText(str(self.PCMPrice))
        self.DoubleSalt_le = QLineEdit()
        self.DoubleSalt_le.setText(str(self.DoubleSalt))
        self.Radio_le = QLineEdit()
        self.Radio_le.setText(str(self.RadioPrice))
        self.Anthenna_le = QLineEdit()
        self.Anthenna_le.setText(str(self.AnthennaPrice))
        self.Modem_le = QLineEdit()
        self.Modem_le.setText(str(self.ModemPrice))
        self.Fiber_le = QLineEdit()
        self.Fiber_le.setText(str(self.FiberPrice))

        self.flo.addRow('PCM - R$', self.PCM_le)
        self.flo.addRow('Double salt - R$', self.DoubleSalt_le)
        self.flo.addRow('Radio - R$', self.Radio_le)
        self.flo.addRow('Anthenna - R$', self.Anthenna_le)
        self.flo.addRow('Modem - R$', self.Modem_le)
        self.flo.addRow('Fiber - R$', self.Fiber_le)

        self.UpdatePricesBtn = QPushButton('Update')
        self.UpdatePricesBtn.clicked.connect(self.UpdatePrices)

        self.VBOX = QVBoxLayout()
        self.VBOX.addLayout(self.flo)
        self.VBOX.addWidget(self.UpdatePricesBtn)

        self.PricesDialog.setLayout(self.VBOX)
        self.PricesDialog.setWindowTitle('Prices window')
        self.PricesDialog.setGeometry(100, 100, 200, 200)
        self.PricesDialog.exec_()

    def UpdatePrices(self):
        self.AnthennaPrice = int(self.Anthenna_le.text())
        self.PCMPrice = int(self.PCM_le.text())
        self.DoubleSalt = int(self.DoubleSalt_le.text())
        self.RadioPrice = int(self.Radio_le.text())
        self.ModemPrice = int(self.Modem_le.text())
        self.FiberPrice = int(self.Fiber_le.text())

    def ShowCppMatrix(self):
        self.OutputCpp = QDialog()
        self.Cpplayout = QGridLayout()

        vertical_placment = 1
        for i in range(2, self.nxn + 2):
            for j in range(2, self.nxn + 2):
                if j > i and self.CppMatrix[i - 2][j - 2] != 0:
                    source = i
                    destiny = j
                    ch_number = self.CppMatrix[i - 2][j - 2]
                    self.Cpplayout.addWidget(QLabel(
                        '{0} to {1}: {2} channels'.format(self.letters[source - 2], self.letters[destiny - 2],
                                                          '{0:.0f}'.format(self.CppMatrix[source - 2][destiny - 2]))),
                                             vertical_placment, 1)
                    vertical_placment += 1

        self.OutputCpp.setLayout(self.Cpplayout)
        self.OutputCpp.setWindowTitle('CPP matrix')
        self.OutputCpp.setGeometry(100, 100, 200, 200)
        self.OutputCpp.exec_()

    def ChannelsPerPath(self):  # Atualizes the number of channels per path in channels matrix
        self.CppMatrix = np.zeros_like(self.DistMatrix)
        self.Graph = []
        for v in range(0, self.nxn):
            self.Graph.append([v, [], 'u', 'u'])  # [station, neighborhood,
            # initial color undefined,
            # initial father station undefined]
        for i in range(0, self.nxn):
            for j in range(0, self.nxn):
                if self.ChannelsMatrix[i][j] != 0:
                    source = i
                    destiny = j
                    self.UpdatesGraph(source)
                    while destiny != source:
                        if self.Graph[destiny][1].count(source) == 0:
                            father = self.Graph[destiny][3]
                            self.CppMatrix[father][destiny] += self.ChannelsMatrix[i][j]
                            destiny = father
                            continue
                        else:
                            if source > destiny:
                                source, destiny = [destiny, source]
                            else:
                                pass
                            self.CppMatrix[source][destiny] += self.ChannelsMatrix[i][j]
                            break
                else:
                    pass

    def UpdateValues(self):
        if self.btnOk.isChecked() or not (self.btnOk.isChecked()):
            self.FreqOp = self.freqOpBox.text()
            self.nxn_bfr = self.nxn
            self.AmountOfCentrals = self.amountCentralsSpinBox.value()
            self.nxn = self.AmountOfCentrals

            # Distances and channels matrix updates if the number of stations has been changed
            if self.nxn == self.nxn_bfr:
                pass
            else:
                self.DistMatrix = np.zeros((self.nxn, self.nxn))
                self.ChannelsMatrix = np.zeros((self.nxn, self.nxn))
                self.CppMatrix = np.zeros((self.nxn, self.nxn))
                self.Graph = []  # Graph reinitialization

                for v in range(0, self.nxn):
                    self.Graph.append(
                        [v, [], 'u', 'u'])  # [station, neighborhood, initial color undefined, father station]

    def UpdateDistMatrix(self):
        if self.DistMatrixUpdateBtn.isChecked() or not (self.DistMatrixUpdateBtn.isChecked()):
            for i in range(2, self.nxn + 2):
                for j in range(2, self.nxn + 2):
                    if (i != j and j > i):
                        self.gridItem = self.DistMatrixDialogGrid.itemAtPosition(i, j)
                        self.tempWidget = self.gridItem.widget()
                        self.DistMatrix[i - 2][j - 2] = self.tempWidget.text()
                    else:
                        pass
        for i in range(0, self.nxn):
            for j in range(0, self.nxn):
                if i > j:
                    self.DistMatrix[i][j] = self.DistMatrix[j][i]
                else:

                    pass
        self.Graph = []
        for v in range(0, self.nxn):
            self.Graph.append([v, [], 'u',
                               'u'])  # [station, neighborhood, initial color undefined, initial father station undefined]

    def UpdatesGraph(self, source):
        self.Graph = []
        for v in range(0, self.nxn):  # Reinitialization
            self.Graph.append(
                [v, [], 'u', 'u'])  # [station, neighborhood, initial color undefined, initial father station undefined]
        for i in range(0, self.nxn):
            for j in range(0, self.nxn):
                if self.DistMatrix[i][j] != 0:
                    self.Graph[i][1].append(j)  # Defines neighborhood
        self.BSF(source)

    # Algorithm for horizontal search
    def BSF(self, source):
        # Initialization
        for station in range(0, self.nxn):  # set colors for the stations and undefined father station
            # print(self.Graph[station][0])
            if self.Graph[station][0] != source:
                self.Graph[station][2] = 'w'  # white
                self.Graph[station][3] = 'u'
            else:  # source station
                self.Graph[station][2] = 'g'  # gray
                self.Graph[station][3] = 'u'
        queue = []
        queue.append(source)
        while len(queue) != 0:
            u = queue.pop(0)
            for neighbor in self.Graph[u][1]:
                if self.Graph[neighbor][2] == 'w':
                    self.Graph[neighbor][2] = 'g'  # changes color of neighbor station to gray
                    self.Graph[neighbor][3] = u
                    queue.append(neighbor)
            self.Graph[u][2] = 'b'

    def ShowDistMatrix(self):
        self.DistMatrixDialog = QDialog()
        self.DistMatrixDialog.setWindowTitle("Distances matrix")
        self.DistMatrixDialogGrid = QGridLayout()
        self.DistMatrixUpdateBtn = QPushButton('Update')
        self.DistMatrixDialogGrid.addWidget(self.DistMatrixUpdateBtn, self.nxn + 2, 1)
        self.DistMatrixUpdateBtn.clicked.connect(self.UpdateDistMatrix)
        for i in range(1, self.nxn + 2):
            for j in range(1, self.nxn + 2):
                if ((i >= 2 and j >= 2) and (i >= j)) or (i == 1 and j == 1):
                    self.DistMatrixDialogGrid.addWidget(QLabel(' - '), i, j)
                elif i == 1 and j != 1:
                    self.DistMatrixDialogGrid.addWidget(QLabel('{0}'.format(self.letters[j - 2])), i, j)
                elif j == 1 and i != 1:
                    self.DistMatrixDialogGrid.addWidget(QLabel('{0}'.format(self.letters[i - 2])), i, j)
                else:
                    try:
                        item = str(int(self.DistMatrix[i - 2][j - 2]))
                        self.DistMatrixDialogGrid.addWidget(QLineEdit(item), i, j)
                    except IndexError:
                        pass

        self.DistMatrixDialog.setLayout(self.DistMatrixDialogGrid)
        self.DistMatrixDialog.setGeometry(100, 100, 200, 200)
        self.DistMatrixDialog.exec_()

    def UpdateChannelsMatrix(self):
        if self.ChannelsMatrixUpdateBtn.isChecked() or not (self.ChannelsMatrixUpdateBtn.isChecked()):
            for i in range(2, self.nxn + 2):
                for j in range(2, self.nxn + 2):
                    if (i != j and j > i):
                        self.gridItem = self.ChannelsMatrixGrid.itemAtPosition(i, j)
                        self.tempWidget = self.gridItem.widget()
                        self.ChannelsMatrix[i - 2][j - 2] = self.tempWidget.text()
                    else:

                        pass
        self.Graph = []
        for v in range(0, self.nxn):
            self.Graph.append([v, [], 'u',
                               'u'])  # [station, neighborhood, initial color undefined, initial father station undefined]

    def ShowChannelsMatrix(self):
        self.ChannelsMatrixDialog = QDialog()
        self.ChannelsMatrixDialog.setWindowTitle("Channels matrix")
        self.ChannelsMatrixGrid = QGridLayout()
        self.ChannelsMatrixUpdateBtn = QPushButton('Update')
        self.ChannelsMatrixGrid.addWidget(self.ChannelsMatrixUpdateBtn, self.nxn + 2, 1)
        self.ChannelsMatrixUpdateBtn.clicked.connect(self.UpdateChannelsMatrix)
        for i in range(1, self.nxn + 2):
            for j in range(1, self.nxn + 2):
                if ((i >= 2 and j >= 2) and (i >= j)) or (i == 1 and j == 1):
                    self.ChannelsMatrixGrid.addWidget(QLabel(' - '), i, j)
                elif i == 1 and j != 1:
                    self.ChannelsMatrixGrid.addWidget(QLabel('{0}'.format(self.letters[j - 2])), i, j)
                elif j == 1 and i != 1:
                    self.ChannelsMatrixGrid.addWidget(QLabel('{0}'.format(self.letters[i - 2])), i, j)
                else:
                    try:
                        item = str(int(self.ChannelsMatrix[i - 2][j - 2]))
                        self.ChannelsMatrixGrid.addWidget(QLineEdit(item), i, j)
                    except IndexError:
                        pass

        self.ChannelsMatrixDialog.setLayout(self.ChannelsMatrixGrid)
        self.ChannelsMatrixDialog.setGeometry(100, 100, 200, 200)
        self.ChannelsMatrixDialog.exec_()

    # This function is responsible for select the best medium of transmission
    # Returns (Radio, Optical fiber without repeater)
    def OForRadio(self):  # Shows paths with distances, Prx for each path and viability
        # Standard free space loss for all paths

        # If the path supports Radio, then the costs will be calculated and compared. Else, optical transmission will
        #  be used.
        self.OForRadioDialog = QDialog()
        self.OForRadioDialog.setWindowTitle("Transmission medium info")
        self.OForRadioDialogGrid = QGridLayout()

        self.Aobs = 8  # Standart obstacle loss for all pathies in dB
        self.Prx = []

        # Prx array computation

        for i in range(0, self.DistMatrix.shape[0] - 1):
            for j in range(1, self.DistMatrix.shape[1]):
                if j > i and self.DistMatrix[i][j] != 0:
                    Prx = 40 + 12 + 12 - (31.5 + 20 * np.log10(int(self.FreqOp)) + 20 * np.log10(
                        int(self.DistMatrix[i][j])) + self.Aobs)
                    WhichOne = 'Both' if Prx > -80 else 'Fiber'
                    self.Prx.append([self.letters[i], self.letters[j], Prx, WhichOne, int(), int()])

        # Shows the results
        vertical_placment = 1
        for path in self.Prx:
            Source = path[0]
            Destiny = path[1]
            Prx = "{0:.2f}".format(path[2])
            WhichOne = path[3]
            Distance = self.DistMatrix[self.letters.index(Source)][self.letters.index(Destiny)]
            AmountOfChannels = self.CppMatrix[self.letters.index(Source)][self.letters.index(Destiny)]
            path[4] = AmountOfChannels
            AmountOfDoubleJumpers = round(round(AmountOfChannels/30)/16)
            path[5] = AmountOfDoubleJumpers
            RadioPrice = AmountOfDoubleJumpers * (2 * self.RadioPrice + 2 * self.AnthennaPrice)
            OpticalPrice = AmountOfDoubleJumpers * (2 * self.ModemPrice + Distance * self.FiberPrice)
            self.OForRadioDialogGrid.addWidget(
                QLabel('{0} to {1} >>> Distance = {2} km | Prx = {3} dBm | OF or Radio: (technical viability) = {4}{5} '
                       .format(Source, Destiny, Distance, Prx, WhichOne,
                               '' if WhichOne == 'Fiber' else (
                                   ", (financial viability) = Radio" if RadioPrice < OpticalPrice
                                   else ", (financial viability) = Fiber"))), vertical_placment, 1)
            path[3] = 'Fiber' if WhichOne == 'Fiber' else 'Radio' if RadioPrice < OpticalPrice else 'Fiber'
            vertical_placment += 1

        self.OForRadioDialog.setLayout(self.OForRadioDialogGrid)
        self.OForRadioDialog.setGeometry(100, 100, 200, 200)
        self.OForRadioDialog.exec_()

def main():
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()