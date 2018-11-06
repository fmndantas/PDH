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
		self.FreqOp = 15000 # in MHz
		self.AmountOfCentrals = 2
		
		# Matrix for distances, channels and LP's
		self.nxn = 2
		self.DistMatrix = np.zeros((self.nxn, self.nxn))
		self.ChannelsMatrix = np.zeros_like(self.DistMatrix)
		self.CppMatrix = np.zeros_like(self.DistMatrix)
		self.LPsMatrix = np.empty((self.nxn, self.nxn))

		# Initializes graph for path finding
		self.Graph = []

		# Initialization of interface
		#self.layout = QFormLayout()

		# Tab try
		# self.tabTogether = QTabWidget()
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

		'''
		self.OutputBtn = QPushButton('Output data')
		self.OutputBtn.clicked.connect(self.ShowOutputMainFrame)
		self.layout.addWidget(self.OutputBtn, 5, 2)
		'''

		self.UpdateLabel = QLabel('')
		self.layout.addWidget(self.UpdateLabel, 6, 1)

		#self.tabTogether.setTabText(0, "Fernando")
		self.setTabText(0, "Input window")
		self.InputWindow.setLayout(self.layout)
		self.setWindowTitle("Input window")

	def OutputWindowTab(self):

		self.layoutOut = QGridLayout()

		'''
		self.DistMatrixBtn = QPushButton('Distance Matrix')
		self.DistMatrixBtn.clicked.connect(self.ShowDistMatrix)
		self.layoutOut.addWidget(self.DistMatrixBtn, 2, 2)

		self.ChannelsAndLpsMatrixBtn = QPushButton('Channels and LP\'s\nmatrix')
		self.ChannelsAndLpsMatrixBtn.clicked.connect(self.ShowChannelsMatrix)
		self.layoutOut.addWidget(self.ChannelsAndLpsMatrixBtn, 3, 2)
		
		self.OutputBtn = QPushButton('Output data')
		self.OutputBtn.clicked.connect(self.ShowOutputMainFrame)
		self.layoutOut.addWidget(self.OutputBtn, 5, 2)
		'''

		self.ChannelsPerPathBtn = QPushButton('Channels per path')
		self.ChannelsPerPathBtn.clicked.connect(self.ChannelsPerPath) # Process and return the Cpp matrix
		self.ChannelsPerPathBtn.clicked.connect(self.ShowCppMatrix) # Shows the Cpp matrix
		self.layoutOut.addWidget(self.ChannelsPerPathBtn, 2, 1)

		self.setTabText(1, "Output window")
		self.OutputWindow.setLayout(self.layoutOut)

	'''
	def ShowOutputMainFrame(self): # Window that pop up when the Output window button is pressed
		self.OutputMainframe = QDialog()
		self.OutputMainframe.setWindowTitle('Output window')
		self.OutputMainframeGrid = QGridLayout()

		#self.SchemeBtn = QPushButton('Show scheme')
		#self.SchemeBtn.clicked.connect(self.ShowScheme)
		#self.OutputMainframeGrid.addWidget(self.SchemeBtn, 1, 1)

		self.ChannelsPerPathBtn = QPushButton('Channels per path')
		self.ChannelsPerPathBtn.clicked.connect(self.ChannelsPerPath) # Process and return the Cpp matrix
		self.ChannelsPerPathBtn.clicked.connect(self.ShowCppMatrix) # Shows the Cpp matrix
		self.OutputMainframeGrid.addWidget(self.ChannelsPerPathBtn, 2, 1)

		self.OutputMainframe.setLayout(self.OutputMainframeGrid)
		self.OutputMainframe.setWindowTitle('Output window')
		self.OutputMainframe.setGeometry(100, 100, 200, 200)
		self.OutputMainframe.exec_()
	'''

	def ShowCppMatrix(self):
		self.OutputCpp = QDialog()
		self.Cpplayout = QGridLayout()

		vertical_placment = 1
		for i in range(2, self.nxn+2):
			for j in range(2, self.nxn+2):
				if j > i and self.CppMatrix[i-2][j-2] != 0:
					source = i
					destiny = j
					ch_number = self.CppMatrix[i-2][j-2]
					self.Cpplayout.addWidget(QLabel('{0} to {1}: {2} channels'.format(self.letters[source-2], self.letters[destiny-2], '{0:.0f}'.format(self.CppMatrix[source-2][destiny-2]))), vertical_placment, 1)
					vertical_placment += 1

		self.OutputCpp.setLayout(self.Cpplayout)
		self.OutputCpp.setWindowTitle('CPP matrix')
		self.OutputCpp.setGeometry(100, 100, 200, 200)
		self.OutputCpp.exec_()

	def ChannelsPerPath(self): # Atualizes the number of channels per path in channels matrix
		self.CppMatrix = np.zeros_like(self.DistMatrix)
		self.Graph = []
		for v in range(0, self.nxn):
			self.Graph.append([v, [], 'u', 'u']) # [station, neighborhood, 
												 #initial color undefined, 
												 #initial father station undefined]
		for i in range(0, self.nxn):
			for j in range(0, self.nxn):
				if self.ChannelsMatrix[i][j] != 0:
					source = i
					destiny = j
					self.UpdatesGraph(source)
					#print(self.CppMatrix)
					#print(self.ChannelsMatrix)
					print('{0} to {1}'.format(self.letters[i], self.letters[j]))
					print(self.Graph)
					# primeira coisa é ver se tem vizinhança direta. se sim, a matriz de canais ja recebe os canais do trecho direto
					# se n tiver vizinhança direta ve o pai e dps ve os nos do pai e nos caminhos achados vai colocando os canais
					while destiny != source:
						if self.Graph[destiny][1].count(source) == 0:
							# Colocar no caminho do pai
								father = self.Graph[destiny][3] # pai do destino
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
		print(self.CppMatrix)
				

	def UpdateValues(self):
		if self.btnOk.isChecked() or not(self.btnOk.isChecked()):
			self.FreqOp = self.freqOpBox.text()
			self.nxn_bfr = self.nxn
			self.AmountOfCentrals = self.amountCentralsSpinBox.value()
			self.nxn = self.AmountOfCentrals
			
			#self.UpdateLabel.setText('Sucessfuly updated')

			# Distances and channels matrix updates if the number of stations has been changed
			if self.nxn == self.nxn_bfr:
				pass
			else:
				self.DistMatrix = np.zeros((self.nxn, self.nxn))
				self.ChannelsMatrix = np.zeros((self.nxn, self.nxn))
				self.CppMatrix = np.zeros((self.nxn, self.nxn))
				self.Graph = [] # Graph reinitialization
				for v in range(0, self.nxn):
					self.Graph.append([v, [], 'u', 'u']) # [station, neighborhood, initial color undefined, father station]

	def UpdateDistMatrix(self):
		if self.DistMatrixUpdateBtn.isChecked() or not(self.DistMatrixUpdateBtn.isChecked()):
			for i in range(2, self.nxn+2):
				for j in range(2, self.nxn+2):
					if (i != j and j > i):
						self.gridItem = self.DistMatrixDialogGrid.itemAtPosition(i, j)
						self.tempWidget = self.gridItem.widget()
						self.DistMatrix[i-2][j-2] = self.tempWidget.text()
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
			self.Graph.append([v, [], 'u', 'u']) # [station, neighborhood, initial color undefined, initial father station undefined]	

	def UpdatesGraph(self, source):
		#print('UPDATES GRAPH')
		self.Graph = []
		for v in range(0, self.nxn): # Reinitialization
			self.Graph.append([v, [], 'u', 'u']) # [station, neighborhood, initial color undefined, initial father station undefined]
		for i in range(0, self.nxn):
			for j in range(0, self.nxn):
				if self.DistMatrix[i][j] != 0:
					self.Graph[i][1].append(j) # Defines neighborhood
		#print(self.Graph)
		self.BSF(source)

	# Algorithm for horizontal search
	def BSF(self, source):
		# Initialization
		for station in range(0, self.nxn): # set colors for the stations and undefined father station
			#print(self.Graph[station][0])
			if self.Graph[station][0] != source:
				self.Graph[station][2] = 'w' # white
				self.Graph[station][3] = 'u'
			else: # source station
				self.Graph[station][2] = 'g' # gray
				self.Graph[station][3] = 'u'
		queue = []
		queue.append(source)
		while len(queue) != 0:
			u = queue.pop(0)
			for neighbor in self.Graph[u][1]:
				if self.Graph[neighbor][2] == 'w':
					self.Graph[neighbor][2] = 'g' # changes color of neighbor station to gray
					self.Graph[neighbor][3] = u 
					queue.append(neighbor)
			self.Graph[u][2] = 'b'

	def ShowDistMatrix(self):
		self.DistMatrixDialog = QDialog()
		self.DistMatrixDialog.setWindowTitle("Distances matrix")
		self.DistMatrixDialogGrid = QGridLayout()
		self.DistMatrixUpdateBtn = QPushButton('Update')
		self.DistMatrixDialogGrid.addWidget(self.DistMatrixUpdateBtn, self.nxn+2, 1)
		self.DistMatrixUpdateBtn.clicked.connect(self.UpdateDistMatrix)
		for i in range(1, self.nxn+2):
			for j in range(1, self.nxn+2):
				if ((i >= 2 and j >= 2) and (i >= j)) or (i == 1 and j == 1):
					self.DistMatrixDialogGrid.addWidget(QLabel(' - '), i, j)
				elif i == 1 and j != 1:
					self.DistMatrixDialogGrid.addWidget(QLabel('{0}'.format(self.letters[j-2])), i, j)
				elif j == 1 and i != 1: 
					self.DistMatrixDialogGrid.addWidget(QLabel('{0}'.format(self.letters[i-2])), i, j)
				else:
					try:
						item = str(int(self.DistMatrix[i-2][j-2]))
						self.DistMatrixDialogGrid.addWidget(QLineEdit(item), i, j)
					except IndexError:
						pass

		self.DistMatrixDialog.setLayout(self.DistMatrixDialogGrid)
		self.DistMatrixDialog.setGeometry(100, 100, 200, 200)
		self.DistMatrixDialog.exec_()

	def UpdateChannelsMatrix(self):
		if self.ChannelsMatrixUpdateBtn.isChecked() or not(self.ChannelsMatrixUpdateBtn.isChecked()):
			for i in range(2, self.nxn+2):
				for j in range(2, self.nxn+2):
					if (i != j and j > i):
						self.gridItem = self.ChannelsMatrixGrid.itemAtPosition(i, j)
						self.tempWidget = self.gridItem.widget()
						self.ChannelsMatrix[i-2][j-2] = self.tempWidget.text()
					else:
						pass
		self.Graph = []
		for v in range(0, self.nxn):
			self.Graph.append([v, [], 'u', 'u']) # [station, neighborhood, initial color undefined, initial father station undefined]
		#print(self.ChannelsMatrix)	

	def ShowChannelsMatrix(self):
		self.ChannelsMatrixDialog = QDialog()
		self.ChannelsMatrixDialog.setWindowTitle("Channels matrix")
		self.ChannelsMatrixGrid = QGridLayout()
		self.ChannelsMatrixUpdateBtn = QPushButton('Update')
		self.ChannelsMatrixGrid.addWidget(self.ChannelsMatrixUpdateBtn, self.nxn+2, 1)
		self.ChannelsMatrixUpdateBtn.clicked.connect(self.UpdateChannelsMatrix)
		for i in range(1, self.nxn+2):
			for j in range(1, self.nxn+2):
				if ((i >= 2 and j >= 2) and (i >= j)) or (i == 1 and j == 1):
					self.ChannelsMatrixGrid.addWidget(QLabel(' - '), i, j)
				elif i == 1 and j != 1:
					self.ChannelsMatrixGrid.addWidget(QLabel('{0}'.format(self.letters[j-2])), i, j)
				elif j == 1 and i != 1: 
					self.ChannelsMatrixGrid.addWidget(QLabel('{0}'.format(self.letters[i-2])), i, j)
				else:
					try:
						item = str(int(self.ChannelsMatrix[i-2][j-2]))
						self.ChannelsMatrixGrid.addWidget(QLineEdit(item), i, j)
					except IndexError:
						pass

		self.ChannelsMatrixDialog.setLayout(self.ChannelsMatrixGrid)
		self.ChannelsMatrixDialog.setGeometry(100, 100, 200, 200)
		self.ChannelsMatrixDialog.exec_()

	# This function is responsible for select the best medium of transmission
	# Returns (Radio, Optical fiber without repeater)
	def OForRadio(self):
		# Standart free space loss for all pathies
		self.Aobs = 5
		for i in range(0, self.DistMatrix.shape[0]-1):
			for j in range(1, self.DistMatrix.shape[1]):
				if j > i and self.DistMatrix[i][j] != 0:
					self.Prx = 31.5 - 20*np.log10(self.FreqOp) - 20*np.log10(DistMatrix[i][j]) 
					if self.DistMatrix[i][j] <= 100 and self.Prx > -80:
						return (True, self.Prx, True)
					elif self.DistMatrix[i][j] > 100 and self.Prx > -80:
						return (True, self.Prx, False)
					else: 
						return (False, self.Prx, False)

def main():
	app = QApplication(sys.argv)
	ex = Interface()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()