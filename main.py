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
        self.showFullScreen()
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

        if username == "" and password == "":
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")



# ------------------ MAIN WINDOW ------------------
class MainWindow(QMainWindow):  #Clase MainWindow heredada de QMainWindow, que es una clase de PyQt para crear la ventana principal de la app.
    def __init__(self): #constructor method. Se ejuecuta cuando la instancia de la clase es creada.
        super().__init__() #llama al constructor de la clase QMainWindow, para inicializar las funcionalidades básicas de la ventana principal de la app.
        self.ui = Ui_MainWindow() #crea una instancia de Ui_MainWindow class, la cual es la definición de la interfaz del usuario para la ventana principal.
        self.ui.setupUi(self) #llama al método setupUi() de la instancia Ui_MainWindow, para setear los componenetes de la interfaz del usuario dentro de main window.

        self.tiempo_credito = 270
        self.tupla_tiempo = (0, 0)

        self.creditos_boxes = []
        self.estado_boxes = [] # 0 es sin conexion, 1 es encendida, 2 es apagada
        self.tiempo_boxes = []
        self.tiempo_total_boxes = []
        self.productos = []
        for i in range(5):
            self.creditos_boxes.append(0)
            self.tiempo_boxes.append((0,0))
            self.tiempo_total_boxes.append(0)
            self.productos.append("")
            self.estado_boxes.append(0)

        self.actualBox = 0 # 0 es 1, 1 es 2, etc...
        self.ui.comboBox.addItems(["BOX1", "BOX2", "BOX3", "BOX4", "BOX5"])
        self.ui.listFree.addItems(["BOX1", "BOX2", "BOX3", "BOX4", "BOX5"])
        self.ui.comboBox.currentIndexChanged.connect(self.cambioBox)

        self.arduino = None
        self.puerto = 'COM3'
        try:
            # revisar a que puerto esta conectado el arduino
            puertos = serial.tools.list_ports.comports()
            for p in puertos:
                if "CH340" in p.description:
                    print(p.device, p.description)
                    self.puerto = p.device
            self.arduino = serial.Serial(self.puerto, 9600)

            time.sleep(5)  # Espera a que se estabilice la conexión
            tiempo_por_cred = f"T{self.tiempo_credito}\n"
            self.arduino.write(tiempo_por_cred.encode())
            print(tiempo_por_cred)
        except:
            print("ERROR: puerto al arduino no localizado. Por favor verifique la conexion.")

        self.timer = QTimer()
        self.estado = QTimer()
        self.timer.timeout.connect(self.leer_serial)
        self.estado.timeout.connect(self.actualizar_estados)
        if self.arduino != None:
            self.timer.start(10)
            self.estado.start(100)

    def creditos(self):
        print("Creditos ingresados:",self.ui.spinCreditos.value())
        creditos_cargados = "C" + str(self.ui.spinCreditos.value())
        self.creditos_boxes[self.actualBox] = self.ui.spinCreditos.value()
        self.arduino.write(creditos_cargados.encode())

    def cambioBox(self, index):
        self.actualBox = index
        print(self.actualBox)

    def separar_num(self, tiempo):
        if "T" in tiempo:
            box_tiempo = tiempo.split("T")
            min_sec = box_tiempo[1].split(":")
            return int(min_sec[0]), int(min_sec[1])
    
    def imprimir_tiempo(self):
        min = str(self.tiempo_boxes[self.actualBox][0])
        sec = str(self.tiempo_boxes[self.actualBox][1])
        if self.tiempo_boxes[self.actualBox][1] < 10:
            sec = "0" + sec
        self.ui.lcdTime.display(f"{min}:{sec}")
    
    def imprimir_producto(self):
        self.ui.agua.setStyleSheet("background-color: white;")
        self.ui.jabon.setStyleSheet("background-color: white;")
        self.ui.foam.setStyleSheet("background-color: white;")
        self.ui.desengrasante.setStyleSheet("background-color: white;")
        self.ui.cera.setStyleSheet("background-color: white;")

        if self.productos[self.actualBox] == 'A':
            self.ui.agua.setStyleSheet("background-color: lightgreen;")
        elif self.productos[self.actualBox] == 'J':
            self.ui.jabon.setStyleSheet("background-color: lightgreen;")
        elif self.productos[self.actualBox] == 'D':
            self.ui.desengrasante.setStyleSheet("background-color: lightgreen;")
        elif self.productos[self.actualBox] == 'F':
            self.ui.foam.setStyleSheet("background-color: lightgreen;")
        elif self.productos[self.actualBox] == 'C':
            self.ui.cera.setStyleSheet("background-color: lightgreen;")

    def barra_porcentaje(self):
        tiempo_total = self.creditos_boxes[self.actualBox] * self.tiempo_credito

        if tiempo_total == 0:
            self.ui.progressTime.setValue(0)
            return

        # tiempo restante -> calcular cuánto se consumió
        tiempo_consumido = tiempo_total - (self.tiempo_boxes[self.actualBox][0] * 60 + self.tiempo_boxes[self.actualBox][1])
        porcentaje = int((tiempo_consumido / tiempo_total) * 100)

        # límites para evitar números fuera de rango
        porcentaje = max(0, min(100, porcentaje))
        self.ui.progressTime.setValue(porcentaje)
    
    def leer_serial(self):
        if self.arduino.in_waiting > 0:
            self.mensaje = self.arduino.readline().decode().strip()
            box = int(self.mensaje[0]) - 1
            if self.estado_boxes[box] == 0:
                self.estado_boxes[box] = 1
            # print(self.mensaje)

            if "T" in self.mensaje:
                self.tupla_tiempo = self.separar_num(self.mensaje)
                self.tiempo_boxes[box] = self.tupla_tiempo
                    
            elif "A" in self.mensaje:
                self.productos[box] = 'A'
            elif "J" in self.mensaje:
                self.productos[box] = 'J'
            elif "D" in self.mensaje:
                self.productos[box] = 'D'
            elif "F" in self.mensaje:
                self.productos[box] = 'F'
            elif "C" in self.mensaje:
                self.productos[box] = 'C'

            self.imprimir_producto()
            self.imprimir_tiempo()
            self.barra_porcentaje()

            # definir estado de cada box
            for i in range(5):
                self.estado_boxes[i] = 0
            if "off" in self.mensaje:
                self.estado_boxes[int(self.mensaje[0])] = 2
            if "on" in self.mensaje:
                self.estado_boxes[int(self.mensaje[0])] = 1




            if self.tiempo_boxes[self.actualBox] == (0, 0):
                self.ui.pushIniciar.setEnabled(True)
                self.ui.groupTimer.hide()
                self.ui.groupWashOptions.hide()
                self.ui.groupQR.hide()
            else:
                self.ui.pushIniciar.setEnabled(False)
                self.ui.groupTimer.show()
                self.ui.groupWashOptions.show()
                self.ui.groupQR.show()




    def actualizar_estados(self):
        self.arduino.write(b'?\n')


# ------------------ MAIN PROGRAM ------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
