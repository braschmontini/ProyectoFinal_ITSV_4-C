import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QTimer
import serial.tools.list_ports
import time
import serial

from ui import Ui_MainWindow
class MainWindow(QMainWindow):  #Clase MainWindow heredada de QMainWindow, que es una clase de PyQt para crear la ventana principal de la app.
    def __init__(self): #constructor method. Se ejuecuta cuando la instancia de la clase es creada.
        super().__init__() #llama al constructor de la clase QMainWindow, para inicializar las funcionalidades básicas de la ventana principal de la app.
        self.ui = Ui_MainWindow() #crea una instancia de Ui_MainWindow class, la cual es la definición de la interfaz del usuario para la ventana principal.
        self.ui.setupUi(self) #llama al método setupUi() de la instancia Ui_MainWindow, para setear los componenetes de la interfaz del usuario dentro de main window.
        print("Probando...")

        self.tiempo_credito = 270
        self.tiempo = 0
        self.creditos_boxes = [0, 0, 0, 0, 0]
        self.tiempo_boxes = [0, 0, 0, 0, 0]
        self.actualBox = 0 # 0 es 1, 1 es 2, etc...
        self.ui.comboBox.addItems(["BOX1", "BOX2", "BOX3", "BOX4", "BOX5"])
        self.ui.comboBox.currentIndexChanged.connect(self.cambioBox)
        # self.ui.agua.setStyleSheet("background-color: red;") # cambiar color de fondo de label

        self.arduino = serial.Serial('COM1', 9600)
        time.sleep(2)  # Espera a que se estabilice la conexión

        # Temporizador para leer datos cada 200 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.leer_serial)
        self.timer.start(10)

    def creditos(self):
        print("Creditos ingresados:",self.ui.spinCreditos.value())
        self.creditos_boxes[self.actualBox] = self.ui.spinCreditos.value()
        self.tiempo_boxes[self.actualBox] = self.creditos_boxes[self.actualBox] * self.tiempo_credito
        print(self.creditos_boxes, self.tiempo_boxes)

    def cambioBox(self, index):
        self.actualBox = index
        print(self.actualBox)
        mensaje = "PRUEBAAA\n"  # El \n ayuda a delimitar el mensaje
        self.arduino.write(mensaje.encode())  # Envía como bytes

    def separar_num(self, tiempo):
        if ":" in tiempo:
            self.min = ""
            for i in tiempo:
                if i == ":":
                    break
                self.min += i
            self.sec = ""
            self.in_sec = False
            for i in tiempo:
                if i == ":":
                    self.in_sec = True
                    continue
                if self.in_sec == True:
                    self.sec += i
            return int(self.min), int(self.sec)
    
    def leer_serial(self):
        if self.arduino.in_waiting > 0:
            self.tiempo = self.arduino.readline().decode().strip() 
            self.ui.lcdTime.display(self.tiempo)

            # Actualiza la barra:
            self.barra_porcentaje(self.tiempo)

    def barra_porcentaje(self, tiempo):
        min, sec = self.separar_num(tiempo)
        tiempo_actual = min * 60 + sec

        tiempo_total = self.tiempo_boxes[self.actualBox]  # total en segundos

        if tiempo_total > 0:
            porcentaje = int((tiempo_actual / tiempo_total) * 100)
            self.ui.progressBar.setValue(porcentaje)

if __name__ == "__main__": #checkea si el script está siendo ejecutado como el prog principal (no importado como un modulo).
    app = QApplication(sys.argv)    # Crea un Qt widget, la cual va ser nuestra ventana.
    window = MainWindow() #crea una intancia de MainWindow 
    window.show()   # IMPORTANT!!!!! la ventanas estan ocultas por defecto.
    sys.exit(app.exec_()) # Start the event loop.