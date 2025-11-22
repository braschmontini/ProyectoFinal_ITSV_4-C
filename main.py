import sys
import serial
import serial.tools.list_ports
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QTimer, Qt, QSize
from PySide6.QtGui import QMovie
from PySide6 import QtCore
from untitled_ui import Ui_LoginWindow 
from ui import Ui_MainWindow
from recuperar_mail import RecuperarWindow


# ------------------ LOGIN WINDOW ------------------
class LoginWindow(QMainWindow):
    def __init__(self):

        self.usuario = ["pepito5", "1234"]

        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        # self.showFullScreen()

        self.ui.lineEdit.setStyleSheet("color: black; background-color: white;")
        self.ui.lineEdit_2.setStyleSheet("color: black; background-color: white;")
        self.ui.loginButton.setStyleSheet("color: black; background-color: white;")
        
    def recuperacion(self):
        self.recuperar_window = RecuperarWindow(self.usuario[0], self.usuario[1])
        self.recuperar_window.show()

    def open_main_window(self):
        self.main_window = MainWindow(self.arduino, self.puerto)
        self.main_window.show()
        self.close()

    def checklogin(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        if username == self.usuario[0] and password == self.usuario[1]:
            gif = QMovie("GIF_Carga.gif")
            gif.setScaledSize(QSize(85, 85))
            self.ui.GIFdeCarga.setMovie(gif)
            gif.start()
            try:
                # revisar a que puerto esta conectado el arduino
                puertos = serial.tools.list_ports.comports()
                for p in puertos:
                    if "CH340" in p.description:
                        print(p.device, p.description)
                        self.puerto = p.device
                self.arduino = serial.Serial(self.puerto, 9600)
            except:
                print("ERROR: puerto al arduino no localizado. Por favor verifique la conexion.")
            QtCore.QTimer.singleShot(5000, self.open_main_window)
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")



# ------------------ MAIN WINDOW ------------------
class MainWindow(QMainWindow):  #Clase MainWindow heredada de QMainWindow, que es una clase de PyQt para crear la ventana principal de la app.
    def __init__(self, arduino = None, puerto = 'COM3'): #constructor method. Se ejuecuta cuando la instancia de la clase es creada.
        super().__init__() #llama al constructor de la clase QMainWindow, para inicializar las funcionalidades básicas de la ventana principal de la app.
        self.ui = Ui_MainWindow() #crea una instancia de Ui_MainWindow class, la cual es la definición de la interfaz del usuario para la ventana principal.
        self.ui.setupUi(self) #llama al método setupUi() de la instancia Ui_MainWindow, para setear los componenetes de la interfaz del usuario dentro de main window.

        self.tiempo_credito = 10
        self.tupla_tiempo = (0, 0)

        self.creditos_boxes = []
        self.estado_boxes = [] # 0 es sin conexion, 1 es encendida, 2 es apagada
        self.estados_anteriores = []
        self.tiempo_boxes = []
        self.tiempo_total_boxes = []
        self.productos = []
        for i in range(5):
            self.creditos_boxes.append(0)
            self.tiempo_boxes.append((0,0))
            self.tiempo_total_boxes.append(0)
            self.productos.append("")
            self.estado_boxes.append(0)
            self.estados_anteriores.append(0)

        self.actualBox = 0 # 0 es 1, 1 es 2, etc...
        self.ui.listBox.addItems(["BOX 1", "BOX 2", "BOX 3", "BOX 4", "BOX 5"])

        self.arduino = arduino
        self.puerto = puerto

        tiempo_por_cred = f"T{self.tiempo_credito}\n"
        self.arduino.write(tiempo_por_cred.encode())
        print(tiempo_por_cred)

        self.timer = QTimer()
        self.estado = QTimer()
        self.timer.timeout.connect(self.leer_serial)
        self.estado.timeout.connect(self.actualizar_estados)
        if self.arduino != None:
            self.timer.start(10)
            self.estado.start(100)

    def creditos(self):
        creditos_cargados = "C" + str(self.ui.spinCreditos.value()) + "\n"
        self.creditos_boxes[self.actualBox] = self.ui.spinCreditos.value()
        self.arduino.write(creditos_cargados.encode())
    
    def cambio_box_lista(self, indice):
        self.actualBox = indice

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

    def actualizar_estados_interfaz(self):
        for i in range(5):
            if self.estado_boxes[i] == 0:
                self.ui.listBox.item(i).setForeground(Qt.GlobalColor.lightGray)
            elif self.estado_boxes[i] == 2:
                self.ui.listBox.item(i).setForeground(Qt.GlobalColor.red)
            elif self.estado_boxes[i] == 1:
                self.ui.listBox.item(i).setForeground(Qt.GlobalColor.green)
    
    def leer_serial(self):
        if self.arduino.in_waiting > 0:
            self.mensaje = self.arduino.readline().decode().strip()
            box = int(self.mensaje[0]) - 1
            if self.estado_boxes[box] == 0:
                self.estado_boxes[box] = 1

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
                if self.tiempo_boxes[int(self.mensaje[0]) - 1] == (0, 0):
                    self.estado_boxes[i] = 0
            if "off" in self.mensaje:
                self.estado_boxes[int(self.mensaje[0]) - 1] = 2
            if not self.tiempo_boxes[int(self.mensaje[0]) - 1] == (0, 0):
                self.estado_boxes[int(self.mensaje[0]) - 1] = 1

            self.actualizar_estados_interfaz()

            if self.tiempo_boxes[self.actualBox] == (0, 0) and self.estado_boxes[self.actualBox] == 2:
                self.ui.pushIniciar.setEnabled(True)
                self.ui.groupTimer.hide()
                self.ui.groupWashOptions.hide()
                self.ui.groupQR.hide()
            elif self.estado_boxes[self.actualBox] == 0:
                self.ui.pushIniciar.setEnabled(False)
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