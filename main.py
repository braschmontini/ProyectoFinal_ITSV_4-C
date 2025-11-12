import sys
import time
import serial
import serial.tools.list_ports
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QTimer
from PySide6 import QtUiTools, QtCore
from login_ui import Ui_LoginWindow 
from ui import Ui_MainWindow

# ------------------ LOGIN WINDOW ------------------
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit.setStyleSheet("color: black; background-color: white;")
        self.ui.lineEdit_2.setStyleSheet("color: black; background-color: white;")
        self.ui.loginButton.setStyleSheet("color: black; background-color: white;")



    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
    def checklogin(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        if username == "pepito5" and password == "1234":
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")



# ------------------ MAIN WINDOW ------------------
class MainWindow(QMainWindow):  #Clase MainWindow heredada de QMainWindow, que es una clase de PyQt para crear la ventana principal de la app.
    def __init__(self): #constructor method. Se ejuecuta cuando la instancia de la clase es creada.
        super().__init__() #llama al constructor de la clase QMainWindow, para inicializar las funcionalidades básicas de la ventana principal de la app.
        self.ui = Ui_MainWindow() #crea una instancia de Ui_MainWindow class, la cual es la definición de la interfaz del usuario para la ventana principal.
        self.ui.setupUi(self) #llama al método setupUi() de la instancia Ui_MainWindow, para setear los componenetes de la interfaz del usuario dentro de main window.
        print("Probando...")

        self.tiempo_credito = 270
        self.tiempo = 0
        self.tupla_tiempo = (0, 0)
        self.creditos_boxes = [0, 0, 0, 0, 0]
        self.tiempo_boxes = [0, 0, 0, 0, 0]
        self.actualBox = 0 # 0 es 1, 1 es 2, etc...
        self.ui.comboBox.addItems(["BOX1", "BOX2", "BOX3", "BOX4", "BOX5"])
        self.ui.comboBox.currentIndexChanged.connect(self.cambioBox)
        # self.ui.agua.setStyleSheet("background-color: red;") # cambiar color de fondo de label

        # revisar a que puerto esta conectado el arduino
        puertos = serial.tools.list_ports.comports()
        for p in puertos:
            print(p.device, p.description)

        self.arduino = serial.Serial('COM4', 9600)
        time.sleep(2)  # Espera a que se estabilice la conexión

        # Temporizador para leer datos cada 200 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.leer_serial)
        self.timer.start(10)

    def creditos(self):
        print("Creditos ingresados:",self.ui.spinCreditos.value())
        creditos_cargados = "C" + str(self.ui.spinCreditos.value())
        self.creditos_boxes[self.actualBox] = self.ui.spinCreditos.value()
        self.tiempo_boxes[self.actualBox] = self.creditos_boxes[self.actualBox] * self.tiempo_credito
        print(self.creditos_boxes, self.tiempo_boxes)
        self.arduino.write(creditos_cargados.encode())

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
    
    def imprimir_tiempo(self, tiempo):
        min = str(self.tupla_tiempo[0])
        sec = str(self.tupla_tiempo[1])
        if self.tupla_tiempo[1] < 10:
            sec = "0" + sec
        self.ui.lcdTime.display(f"{min}:{sec}")

    def barra_porcentaje(self):
        tiempo_total = self.tiempo_boxes[self.actualBox]

        if tiempo_total == 0:
            self.ui.progressTime.setValue(0)
            return

        # tiempo restante -> calcular cuánto se consumió
        tiempo_consumido = tiempo_total - (self.tupla_tiempo[0] * 60 + self.tupla_tiempo[1])
        porcentaje = int((tiempo_consumido / tiempo_total) * 100)

        # límites para evitar números fuera de rango
        porcentaje = max(0, min(100, porcentaje))

        self.ui.progressTime.setValue(porcentaje)
    
    def leer_serial(self):
        if self.arduino.in_waiting > 0:
            self.mensaje = self.arduino.readline().decode().strip() 
            if ":" in self.mensaje:
                self.tupla_tiempo = self.separar_num(self.mensaje)
                self.imprimir_tiempo(self.mensaje)
                self.barra_porcentaje()
            elif self.mensaje == "A":
                self.ui.agua.setStyleSheet("background-color: lightgreen;") # <--
                self.ui.jabon.setStyleSheet("background-color: white;")
                self.ui.foam.setStyleSheet("background-color: white;")
                self.ui.desengrasante.setStyleSheet("background-color: white;")
                self.ui.cera.setStyleSheet("background-color: white;")
            elif self.mensaje == "J":
                self.ui.agua.setStyleSheet("background-color: white;")
                self.ui.jabon.setStyleSheet("background-color: lightgreen;") # <--
                self.ui.foam.setStyleSheet("background-color: white;")
                self.ui.desengrasante.setStyleSheet("background-color: white;")
                self.ui.cera.setStyleSheet("background-color: white;")
            elif self.mensaje == "D":
                self.ui.agua.setStyleSheet("background-color: white;")
                self.ui.jabon.setStyleSheet("background-color: white;") 
                self.ui.foam.setStyleSheet("background-color: white;")
                self.ui.desengrasante.setStyleSheet("background-color: lightgreen;") # <--
                self.ui.cera.setStyleSheet("background-color: white;")
            elif self.mensaje == "F":
                self.ui.agua.setStyleSheet("background-color: white;")
                self.ui.jabon.setStyleSheet("background-color: white;") 
                self.ui.foam.setStyleSheet("background-color: lightgreen;") # <--
                self.ui.desengrasante.setStyleSheet("background-color: white;")
                self.ui.cera.setStyleSheet("background-color: white;")
            elif self.mensaje == "C":
                self.ui.agua.setStyleSheet("background-color: white;")
                self.ui.jabon.setStyleSheet("background-color: white;") 
                self.ui.foam.setStyleSheet("background-color: white;")
                self.ui.desengrasante.setStyleSheet("background-color: white;")
                self.ui.cera.setStyleSheet("background-color: lightgreen;") # <--


# ------------------ MAIN PROGRAM ------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
