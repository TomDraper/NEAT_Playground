from PySide6 import QtCore, QtWidgets, QtGui
from neat_playground.data.scenario import Scenario

class RunWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.root = QtWidgets.QVBoxLayout(self)
        self.title = QtWidgets.QLabel("TITLE")
        #self.run_panel = QtWidgets.QFrame(self)
        self.loading_bar = QtWidgets.QProgressBar()
        self.root.addChildWidget(self.title)
        #self.root.addChildWidget(self.run_panel)
        self.root.addChildWidget(self.loading_bar)

    def set_title(self, title):
        self.title.setText(title)

    def set_loading_percent(self, percent:int):
        self.loading_bar.setValue(percent)