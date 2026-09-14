from PySide6 import QtCore, QtWidgets


class DebugCombo(QtWidgets.QComboBox):
    def showPopup(self):
        print("\n--- BEFORE showPopup ---")
        print("App active:", QtWidgets.QApplication.activeWindow())
        print("Combo focus:", self.hasFocus())
        print("Combo window active:", self.window().isActiveWindow())

        super().showPopup()

        print("\n--- AFTER showPopup ---")
        print("App active:", QtWidgets.QApplication.activeWindow())
        print("Combo focus:", self.hasFocus())
        print("Combo window active:", self.window().isActiveWindow())

        print("\n--- TOP LEVEL WINDOWS ---")
        for w in QtWidgets.QApplication.topLevelWidgets():
            print(
                repr(w),
                "visible=", w.isVisible(),
                "active=", w.isActiveWindow(),
                "flags=", w.windowFlags()
            )

    def hidePopup(self):
        print("\n--- hidePopup ---")
        print("App active:", QtWidgets.QApplication.activeWindow())
        super().hidePopup()


app = QtWidgets.QApplication([])

app.applicationStateChanged.connect(
    lambda state: print("APPLICATION STATE:", state)
)

window = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout(window)

combo = DebugCombo()
combo.addItems([
    "Config 1",
    "Config 2",
    "Config 3",
])

layout.addWidget(combo)

window.resize(400, 200)
window.show()

app.exec()