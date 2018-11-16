import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np


class Interface(QTabWidget):
    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)

        self.letters = "ABCDEFGHIJ"

        # Operation frequency of transceptors in KHz and amount of centrals
        self.FreqOp = 15000  # in MHz

        # Matrix for distances, channels and LP's
        self.size = 2
        self.DistMatrix = np.zeros((self.size, self.size))
        self.ChannelsMatrix = np.zeros_like(self.DistMatrix)
        self.ChannelsPerPathMatrix = np.zeros_like(self.DistMatrix)
        self.LPsMatrix = np.empty((self.size, self.size))

        # Initializes graph for path finding and power array
        self.Graph = []
        self.PowerReceptionArray = []

        # Default prices
        self.PCMPrice = 5000
        self.DoubleSaltPrice = 8000
        self.RadioPrice = 80000
        self.AnthennaPrice = 5000
        self.ModemPrice = 4000
        self.FiberPrice = 15000 # Per km

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

        self.sizeLabel = QLabel('Quantity of stations:')
        self.layout.addWidget(self.sizeLabel, 3, 1)

        # Min: 2, Max: 9
        self.sizeSpinBox = QSpinBox()
        self.sizeSpinBox.setMaximum(9)
        self.sizeSpinBox.setMinimum(2)
        self.layout.addWidget(self.sizeSpinBox, 4, 1)

        self.btnOk = QPushButton('Update properties')
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
        self.ChannelsPerPathBtn.clicked.connect(self.ShowChannelsPerPathMatrix)  # Shows the Cpp matrix
        self.layoutOut.addWidget(self.ChannelsPerPathBtn, 2, 1)

        self.of_or_radioBtn = QPushButton('Transmission medium')
        self.of_or_radioBtn.clicked.connect(self.of_or_radio)
        self.of_or_radioBtn.clicked.connect(self.of_or_radio_display)
        self.layoutOut.addWidget(self.of_or_radioBtn, 3, 1)

        self.BudgetBtn = QPushButton('Budget window')
        self.BudgetBtn.clicked.connect(self.ChannelsPerPath)
        self.BudgetBtn.clicked.connect(self.of_or_radio)
        # print('ok')
        self.BudgetBtn.clicked.connect(self.Budget)
        self.layoutOut.addWidget(self.BudgetBtn, 4, 1)

        self.setTabText(1, "Output window")
        self.OutputWindow.setLayout(self.layoutOut)

    def PricesTableDialog(self):
        self.PricesDialog = QDialog()
        self.PricesDialog.setWindowTitle("Channels matrix")

        self.flo = QFormLayout()

        self.PCM_le = QLineEdit()
        self.PCM_le.setText(str(self.PCMPrice))
        self.DoubleSaltPrice_le = QLineEdit()
        self.DoubleSaltPrice_le.setText(str(self.DoubleSaltPrice))
        self.Radio_le = QLineEdit()
        self.Radio_le.setText(str(self.RadioPrice))
        self.Anthenna_le = QLineEdit()
        self.Anthenna_le.setText(str(self.AnthennaPrice))
        self.Modem_le = QLineEdit()
        self.Modem_le.setText(str(self.ModemPrice))
        self.Fiber_le = QLineEdit()
        self.Fiber_le.setText(str(self.FiberPrice))

        self.flo.addRow('PCM - R$', self.PCM_le)
        self.flo.addRow('Double salt - R$', self.DoubleSaltPrice_le)
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
        self.DoubleSaltPrice = int(self.DoubleSaltPrice_le.text())
        self.RadioPrice = int(self.Radio_le.text())
        self.ModemPrice = int(self.Modem_le.text())
        self.FiberPrice = int(self.Fiber_le.text())

    def ShowChannelsPerPathMatrix(self):
        self.OutputCpp = QDialog()
        self.Cpplayout = QGridLayout()

        vertical_placment = 1
        for i in range(2, self.size + 2):
            for j in range(2, self.size + 2):
                if j > i and self.ChannelsPerPathMatrix[i - 2][j - 2] != 0:
                    source = i
                    destiny = j
                    ch_number = self.ChannelsPerPathMatrix[i - 2][j - 2]
                    self.Cpplayout.addWidget(QLabel(
                        '{0} to {1}: {2} channels'.format(self.letters[source - 2], self.letters[destiny - 2],
                                                          '{0:.0f}'.format(self.ChannelsPerPathMatrix[source - 2][destiny - 2]))),
                        vertical_placment, 1)
                    vertical_placment += 1

        self.OutputCpp.setLayout(self.Cpplayout)
        self.OutputCpp.setWindowTitle('CPP matrix')
        self.OutputCpp.setGeometry(100, 100, 200, 200)
        self.OutputCpp.exec_()

    def ChannelsPerPath(self):  # Atualizes the number of channels per path in channels matrix
        self.ChannelsPerPathMatrix = np.zeros_like(self.DistMatrix)
        self.Graph = []
        for v in range(0, self.size):
            self.Graph.append([v, [], 'u', 'u'])  # [station, neighborhood,
            # initial color undefined,
            # initial father station undefined]
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.ChannelsMatrix[i][j] != 0:
                    source = i
                    destiny = j
                    self.UpdatesGraph(source)
                    while destiny != source:
                        if self.Graph[destiny][1].count(source) == 0:
                            father = self.Graph[destiny][3]
                            self.ChannelsPerPathMatrix[father][destiny] += self.ChannelsMatrix[i][j]
                            destiny = father
                            continue
                        else:
                            if source > destiny:
                                source, destiny = [destiny, source]
                            else:
                                pass
                            self.ChannelsPerPathMatrix[source][destiny] += self.ChannelsMatrix[i][j]
                            break
                else:
                    pass

    def UpdateValues(self):
        if self.btnOk.isChecked() or not (self.btnOk.isChecked()):
            self.FreqOp = self.freqOpBox.text()
            self.size_bfr = self.size
            self.size = self.sizeSpinBox.value()

            # Distances and channels matrix updates if the number of stations has been changed
            if self.size == self.size_bfr:
                pass
            else:
                self.DistMatrix = np.zeros((self.size, self.size))
                self.ChannelsMatrix = np.zeros((self.size, self.size))
                self.ChannelsPerPathMatrix = np.zeros((self.size, self.size))
                self.Graph = []  # Graph reinitialization

                for v in range(0, self.size):
                    self.Graph.append(
                        [v, [], 'u', 'u'])  # [station, neighborhood, initial color undefined, father station]

    def UpdateDistMatrix(self):
        if self.DistMatrixUpdateBtn.isChecked() or not (self.DistMatrixUpdateBtn.isChecked()):
            for i in range(2, self.size + 2):
                for j in range(2, self.size + 2):
                    if (i != j and j > i):
                        self.gridItem = self.DistMatrixDialogGrid.itemAtPosition(i, j)
                        self.tempWidget = self.gridItem.widget()
                        self.DistMatrix[i - 2][j - 2] = self.tempWidget.text()
                    else:
                        pass
        for i in range(0, self.size):
            for j in range(0, self.size):
                if i > j:
                    self.DistMatrix[i][j] = self.DistMatrix[j][i]
                else:

                    pass
        self.Graph = []
        for v in range(0, self.size):
            self.Graph.append([v, [], 'u',
                               'u'])  # [station, neighborhood, initial color undefined, initial father station undefined]

    def UpdatesGraph(self, source):
        """

        Calls BFS

        Parameters
        ----------
        source: int
            station


        """
        self.Graph = []
        for v in range(0, self.size):  # Reinitialization
            self.Graph.append(
                [v, [], 'u', 'u'])  # [station, neighborhood, initial color undefined, initial father station undefined]
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.DistMatrix[i][j] != 0:
                    self.Graph[i][1].append(j)  # Defines neighborhood
        self.BFS(source)

    # Algorithm for horizontal search
    def BFS(self, source):
        """Breadth First Search

        Parameters
        ----------
        source: int

        """
        # Initialization
        for station in range(0, self.size):  # set colors for the stations and undefined father station
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
        self.DistMatrixDialogGrid.addWidget(self.DistMatrixUpdateBtn, self.size + 2, 1)
        self.DistMatrixUpdateBtn.clicked.connect(self.UpdateDistMatrix)
        for i in range(1, self.size + 2):
            for j in range(1, self.size + 2):
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
            for i in range(2, self.size + 2):
                for j in range(2, self.size + 2):
                    if (i != j and j > i):
                        self.gridItem = self.ChannelsMatrixGrid.itemAtPosition(i, j)
                        self.tempWidget = self.gridItem.widget()
                        self.ChannelsMatrix[i - 2][j - 2] = self.tempWidget.text()
                    else:
                        pass
        self.Graph = []
        for v in range(0, self.size):
            self.Graph.append([v, [], 'u', 'u'])

        """data structure: [station, neighborhood, initial color undefined, initial father station undefined]"""

    def ShowChannelsMatrix(self):
        self.ChannelsMatrixDialog = QDialog()
        self.ChannelsMatrixDialog.setWindowTitle("Channels matrix")
        self.ChannelsMatrixGrid = QGridLayout()
        self.ChannelsMatrixUpdateBtn = QPushButton('Update')
        self.ChannelsMatrixGrid.addWidget(self.ChannelsMatrixUpdateBtn, self.size + 2, 1)
        self.ChannelsMatrixUpdateBtn.clicked.connect(self.UpdateChannelsMatrix)
        for i in range(1, self.size + 2):
            for j in range(1, self.size + 2):
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
    def of_or_radio(self):  # Shows paths with distances, Prx for each path and viability
        # Standard free space loss for all paths

        # If the path supports Radio, then the costs will be calculated and compared. Else, optical transmission will
        #  be used.

        # Updates
        self.UpdateDistMatrix()
        self.UpdateChannelsMatrix()
        self.ChannelsPerPath()

        self.Aobs = 8  # Standard obstacle loss for all paths in dB
        self.PowerReceptionArray = []

        # Prx array computation
        for i in range(0, self.DistMatrix.shape[0] - 1):
            for j in range(1, self.DistMatrix.shape[1]):
                if j > i and self.DistMatrix[i][j] != 0:
                    Prx = 40 + 12 + 12 - (31.5 + 20 * np.log10(int(self.FreqOp)) + 20 * np.log10(
                        int(self.DistMatrix[i][j])) + self.Aobs)
                    WhichOne = 'Both' if Prx > -80 else 'Fiber'
                    self.PowerReceptionArray.append([self.letters[i], self.letters[j], Prx, WhichOne, '', ''])

        for path in self.PowerReceptionArray:
            Source = path[0]
            Destiny = path[1]
            Distance = self.DistMatrix[self.letters.index(Source)][self.letters.index(Destiny)]
            path[4] = self.ChannelsPerPathMatrix[self.letters.index(Source)][self.letters.index(Destiny)] # Amount of channels update
            path[5] = 2 * path[4] // 30 // 16 # Amount of double jumpers
            RadioPrice = path[5] * (self.RadioPrice + self.AnthennaPrice)
            OpticalPrice = path[5] * (self.ModemPrice + (Distance * self.FiberPrice)/2)
            path[3] = 'Fiber' if path[3] == 'Fiber' else 'Radio' if RadioPrice < OpticalPrice else 'Fiber'

    def of_or_radio_display(self):
        """ Only shows paths with distances, reception power for each path and viability"""

        # Standard free space loss for all paths

        # If the path supports Radio, then the costs will be calculated and compared. Else, optical transmission will
        #  be used.
        self.of_or_radio_dialog = QDialog()
        self.of_or_radio_dialog.setWindowTitle("Transmission medium info")
        self.of_or_radio_dialog_grid = QGridLayout()

        # Shows the results

        vertical_placment = 1
        for path in self.PowerReceptionArray:
            Source = path[0]
            Destiny = path[1]
            Prx = "{0:.2f}".format(path[2])
            WhichOne = path[3]
            Distance = self.DistMatrix[self.letters.index(Source)][self.letters.index(Destiny)]
            self.of_or_radio_dialog_grid.addWidget(
                QLabel('{0} to {1} >>> Distance = {2} km | Prx = {3} dBm | OF or Radio: {4}'
                       .format(Source, Destiny, Distance, Prx, WhichOne)), vertical_placment, 1)
            vertical_placment += 1

        self.of_or_radio_dialog.setLayout(self.of_or_radio_dialog_grid)
        self.of_or_radio_dialog.setGeometry(100, 100, 200, 200)
        self.of_or_radio_dialog.exec_()

    def Budget(self):
        self.BudgetUI = QDialog()
        self.BudgetUI.setWindowTitle('Budget UI')

        self.BudgetLayout = QVBoxLayout()

        self.BudgetTable()

        self.BudgetLayout.addWidget(self.BudgetTableW)
        self.BudgetUI.setLayout(self.BudgetLayout)
        self.BudgetUI.showFullScreen()
        self.BudgetUI.exec_()

    def BudgetTable(self):

        self.BudgetTableW = QTableWidget()
        self.BudgetTableW.setRowCount(20)
        self.BudgetTableW.setColumnCount(5)

        self.Stations = list()
        for i in range(0, self.size):
            self.Stations.append([self.letters[i], 0, 0, 0, 0, 0])

            """
            --------------------------------------------------------------------
            the structure is of self.Station is
                             [0 - name, 1 - total_channels , 2 - double_jumpers, 
                              3 - radio, 4 - anthenna, 5 - modem] 
            --------------------------------------------------------------------
            """

        # Per station elements finder
        for i in range(0, self.size):
            transmission_medium = list()
            for path in self.PowerReceptionArray:
                if path[0] == self.letters[i] or path[1] == self.letters[i]:

                    self.Stations[i][1] += path[4] # Canais
                    transmission_medium.append(path[3])
                else:
                    pass
            self.Stations[i][2] = self.Stations[i][1]//30//16 # Total de duplos saltos
            if self.Stations[i][2] < 1:
                self.Stations[i][2] = 1
            else:
                pass
            for medium in transmission_medium:
                if medium == 'Radio':
                    self.Stations[i][3] += 1 # Medium

                else:
                    pass

            self.Stations[i][4] = self.Stations[i][3]
            self.Stations[i][5] = self.Stations[i][2] - self.Stations[i][4]


        self.equipment_subtotals = [0, 0, 0, 0]

        """
        -------------------------------------------------------------------
        the structure is of self.equipment_subtotals is
                             [0 - double jumpers, 1 - radio , 2 - anthenna, 
                              3 - modem]
        -------------------------------------------------------------------
        """

        # equipment subtotals
        for station in self.Stations:
            self.equipment_subtotals[0] += station[2] # Double jumbers
            self.equipment_subtotals[1] += station[3] # Radio
            self.equipment_subtotals[2] += station[4] # Anthenna
            self.equipment_subtotals[3] += station[5] # Modem

        # price subtotals
        self.prices_subtotals = self.equipment_subtotals.copy()
        self.prices_subtotals[0] *= self.DoubleSaltPrice
        self.prices_subtotals[1] *= self.RadioPrice
        self.prices_subtotals[2] *= self.AnthennaPrice
        self.prices_subtotals[3] *= self.ModemPrice

        # price total
        self.price_total = sum(self.prices_subtotals)

        # fiber price per path

        self.fiber_price_data = []
        """data structure: [origin, destiny], 2*Distance, self.FiberPrice, subtotal"""

        for path in self.PowerReceptionArray:
            same_node_occurrences = 0
            # print(path)
            distance = self.DistMatrix[self.letters.index(path[0])][self.letters.index(path[1])]
            if path[3] == 'Fiber':
                for j in range(0, len(self.PowerReceptionArray)):
                    same_node_occurrences += self.PowerReceptionArray[j][0].count(path[0])
                self.fiber_price_data.append(["{0}-{1}".format(path[0], path[1]),
                                        same_node_occurrences*distance,
                                        self.FiberPrice,
                                        same_node_occurrences*distance*self.FiberPrice])
            else:
                self.fiber_price_data.append(["{0}-{1}".format(path[0], path[1]),
                                              '-----',
                                              self.FiberPrice,
                                              '-----'])
        # print(self.fiber_price_data)

        # Cria os labels da primeira tabela
        for i in range(0, self.size):
            self.BudgetTableW.setItem(i + 1, 0, QTableWidgetItem('Estação {0}'.format(self.letters[i])))

        self.BudgetTableW.setItem(self.size + 1, 0, QTableWidgetItem('Qtd. Total'))
        self.BudgetTableW.setItem(self.size + 2, 0, QTableWidgetItem('Preço unitário (R$)'))
        self.BudgetTableW.setItem(self.size + 3, 0, QTableWidgetItem('Sub-total I (R$)'))
        self.BudgetTableW.setItem(self.size + 4, 0, QTableWidgetItem('Total I (R$)'))
        landscape_labels = ['PCM 30 (qtd.)', 'Duplo salto', 'Radio 480 canais (qtd.)',
                            'Antena SHF (qtd.)', 'Modem óptico (qtd)']
        column_width = 150
        for i in range(0, 5):
            self.BudgetTableW.setColumnWidth(i, column_width)
        for j in range(1, 5):
            self.BudgetTableW.setItem(0, j, QTableWidgetItem(landscape_labels[j]))

        """ Segunda tabela (labels)  """
        landscape_labels_2 = ['Trecho', 'kms', 'Preço por km', 'Subtotal']
        for j in range(0, 4):
            self.BudgetTableW.setItem(self.size + 6, j, QTableWidgetItem(landscape_labels_2[j]))

        fiber_price_item = 0
        for i in range(self.size + 7, self.size + len(self.PowerReceptionArray) + 7):
            for j in range(0, 4):
                self.BudgetTableW.setItem(i, j, QTableWidgetItem(str(self.fiber_price_data[fiber_price_item][j])))
            fiber_price_item += 1

        self.BudgetTableW.setItem(self.size + len(self.PowerReceptionArray) + 8, 0, QTableWidgetItem('Total (R$)'))
        # print(self.price_total)
        self.total = self.price_total
        for item in self.fiber_price_data:
            if type(item[3]) != str:
                self.total += item[3]
            else:
                pass
        self.BudgetTableW.setItem(self.size + len(self.PowerReceptionArray) + 8, 1, QTableWidgetItem(str(self.total)))


        # Preenche a tabela com os dados 'por estação'
        for table_line in range(0, self.size):
            for table_column in range(0, 4):
                self.BudgetTableW.setItem(table_line + 1,
                                          table_column + 1,
                                          QTableWidgetItem('{0:.0f}'.format(self.Stations[table_line][table_column+2])))

        # Mostra dados para a linha "Qtd. total "
        for table_column in range(0, 4):
            self.BudgetTableW.setItem(self.size + 1,
                                      table_column + 1,
                                      QTableWidgetItem(str('{0:.0f}'.format(self.equipment_subtotals[table_column]))))

        # Mostra dados para a linha "Preço unitário"
        self.BudgetTableW.setItem(self.size + 2, 1, QTableWidgetItem(str('{0:.2f}'.format(self.DoubleSaltPrice))))
        self.BudgetTableW.setItem(self.size + 2, 2, QTableWidgetItem(str('{0:.2f}'.format(self.RadioPrice))))
        self.BudgetTableW.setItem(self.size + 2, 3, QTableWidgetItem(str('{0:.2f}'.format(self.AnthennaPrice))))
        self.BudgetTableW.setItem(self.size + 2, 4, QTableWidgetItem(str('{0:.2f}'.format(self.ModemPrice))))

        # Mostra dados para a linha "Sub-total"
        for table_column in range(0, 4):
            self.BudgetTableW.setItem(self.size + 3, table_column + 1,
                                      QTableWidgetItem(str('{0:.2f}'.format(self.prices_subtotals[table_column]))))

        # Mostra dados para a linha "Total"

        self.BudgetTableW.setItem(self.size + 4, 1, QTableWidgetItem(str('{0:.2f}'.format(self.price_total))))

        """
        Segunda tabela
        | Trecho | Kms | Preço por Kms | Subtotal |
        -------------------------------------------
        ...
        -------------------------------------------
        | Sub-total | ... | - | ...
        | Total |
        """


def main():
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
