import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QComboBox
from PySide2.QtCore import Qt

from ui_comboB import Ui_MainWindow

class MainWindow(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self) 

        self.setWindowTitle("My App")

        self.ui.comboBox.addItems(["Fideos", "Polenta", "Asado", "cualquier cosa"])
        self.ui.comboBox.setEditable(True)
        self.ui.comboBox.setMaxCount(6)
        self.ui.comboBox.setInsertPolicy(QComboBox.InsertAlphabetically)

    def index_changed(self, i):  # i is an int
        print(i)

    def text_changed(self, s):  # s is a str
        print(s)

    def click(self):
        self.ui.label.setText(f'Usted seleccionó: {self.ui.comboBox.currentText()}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())