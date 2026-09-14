import sys
from PySide6 import QtCore, QtWidgets, QtGui
from components.mainmenubutton import *

class MainMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel("NEAT Playground", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.subtitle = QtWidgets.QLabel("Scenarios")
        self.button = QtWidgets.QPushButton("Click Me!")
        self.buttons = [
            MainMenuButton("Test Scenario 1", ["Config 1", "Config 2", "Config 3"], "Test Description 1"),
            MainMenuButton("Test Scenario 2", ["Config 4", "Config 5", "Config 6"], "Test Description 2")
        ]

        self.root = QtWidgets.QVBoxLayout(self)
        self.root.addWidget(self.title)
        self.root.addWidget(self.subtitle)
        for button in self.buttons:
            self.root.addWidget(button)

        self.button.clicked.connect(self.print_test)

    @QtCore.Slot()
    def print_test(self):
        print("Yes worked.")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainMenu()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())