import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

"""
from Archivo convertido con pyside2-uic archivo.ui > interfaz.py
import nombre de la clase del archivo convertido
"""
from ui import Ui_MainWindow
class MainWindow(QMainWindow):  #Clase MainWindow heredada de QMainWindow, que es una clase de PyQt para crear la ventana principal de la app.
    def __init__(self): #constructor method. Se ejuecuta cuando la instancia de la clase es creada.
        super().__init__() #llama al constructor de la clase QMainWindow, para inicializar las funcionalidades básicas de la ventana principal de la app.
        self.ui = Ui_MainWindow() #crea una instancia de Ui_MainWindow class, la cual es la definición de la interfaz del usuario para la ventana principal.
        self.ui.setupUi(self) #llama al método setupUi() de la instancia Ui_MainWindow, para setear los componenetes de la interfaz del usuario dentro de main window.
        print("Probando...")
        self.tiempo_credito = 270
        self.creditos_boxes = [0, 0, 0, 0, 0]
        self.tiempo_boxes = [0, 0, 0, 0, 0]
        self.actualBox = 0 # 0 es 1, 1 es 2, etc...
        self.ui.comboBox.addItems(["BOX1", "BOX2", "BOX3", "BOX4", "BOX5"])
        self.ui.comboBox.currentIndexChanged.connect(self.cambioBox)
        # self.ui.agua.setStyleSheet("background-color: red;") # cambiar color de fondo de label


    def creditos(self):
        print("Creditos ingresados:",self.ui.spinCreditos.value())
        self.creditos_boxes[self.actualBox] = self.ui.spinCreditos.value()
        self.tiempo_boxes[self.actualBox] = self.creditos_boxes[self.actualBox] * self.tiempo_credito
        print(self.creditos_boxes, self.tiempo_boxes)

    def cambioBox(self, index):
        self.actualBox = index
        print(self.actualBox)

if __name__ == "__main__": #checkea si el script está siendo ejecutado como el prog principal (no importado como un modulo).
    app = QApplication(sys.argv)    # Crea un Qt widget, la cual va ser nuestra ventana.
    window = MainWindow() #crea una intancia de MainWindow 
    window.show()   # IMPORTANT!!!!! la ventanas estan ocultas por defecto.
    sys.exit(app.exec_()) # Start the event loop.