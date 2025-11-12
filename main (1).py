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
class MainWindow(QMainWindow):  # Tu código original + interfaz de Arduino
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print("Probando...")

        self.tiempo_credito = 270
        self.tiempo = 0
        self.tupla_tiempo = (0, 0)
        self.creditos_boxes = [0, 0, 0, 0, 0]
        self.tiempo_boxes = [0, 0, 0, 0, 0]
        self.actualBox = 0  # 0 es 1, 1 es 2, etc...

        self.ui.comboBox.addItems(["BOX1", "BOX2", "BOX3", "BOX4", "BOX5"])
        self.ui.comboBox.currentIndexChanged.connect(self.cambioBox)

        # Puertos disponibles
        puertos = serial.tools.list_ports.comports()
        for p in puertos:
            print(p.device, p.description)

        # Conectar Arduino
        try:
            self.arduino = serial.Serial('COM4', 9600)
            time.sleep(2)
            print("Conectado al Arduino en COM4")
        except serial.SerialException:
            self.arduino = None
            print("No se pudo conectar al Arduino")

        # Temporizador para leer datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.leer_serial)
        self.timer.start(100)

        # Botón de créditos
        self.ui.pushIniciar.clicked.connect(self.creditos)

    # ------------------ Funciones originales ------------------

    def creditos(self):
        print("Créditos ingresados:", self.ui.spinCreditos.value())
        creditos_cargados = self.ui.spinCreditos.value()
        self.creditos_boxes[self.actualBox] = creditos_cargados
        self.tiempo_boxes[self.actualBox] = self.creditos_boxes[self.actualBox] * self.tiempo_credito
        print(self.creditos_boxes, self.tiempo_boxes)
        if self.arduino:
            self.arduino.write(f"{creditos_cargados}\n".encode())

    def cambioBox(self, index):
        self.actualBox = index
        print(self.actualBox)
        if self.arduino:
            mensaje = f"BOX{index + 1}\n"
            self.arduino.write(mensaje.encode())

    def separar_num(self, tiempo):
        if ":" in tiempo:
            partes = tiempo.split(":")
            if len(partes) == 2:
                return int(partes[0]), int(partes[1])
        return 0, 0

    def imprimir_tiempo(self):
        minutos = str(self.tupla_tiempo[0])
        segundos = str(self.tupla_tiempo[1]).zfill(2)
        self.ui.lcdTime.display(f"{minutos}:{segundos}")

    def leer_serial(self):
        if self.arduino and self.arduino.in_waiting > 0:
            self.tiempo = self.arduino.readline().decode(errors="ignore").strip()
            self.tupla_tiempo = self.separar_num(self.tiempo)
            self.imprimir_tiempo()


# ------------------ MAIN PROGRAM ------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
