import sys
import time
import serial
import serial.tools.list_ports
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QTimer
from PySide6 import QtUiTools, QtCore
from login_ui import Ui_LoginWindow 
from ui import Ui_MainWindow

#Recuperacion de contraseña y usuario
import sys
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# Importa los módulos de PyQt5 necesarios para la Interfaz de Usuario
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog
from PyQt6.QtCore import Qt

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

        self.tiempo_credito = 30
        self.tiempo = 0
        self.tupla_tiempo = (0, 0)

        self.creditos_boxes = []
        self.tiempo_boxes = []
        self.tiempo_total_boxes = []
        for i in range(5):
            self.creditos_boxes.append(0)
            self.tiempo_boxes.append((0,0))
            self.tiempo_total_boxes.append(0)

        self.actualBox = 0 # 0 es 1, 1 es 2, etc...
        self.ui.comboBox.addItems(["BOX1", "BOX2", "BOX3", "BOX4", "BOX5"])
        self.ui.comboBox.currentIndexChanged.connect(self.cambioBox)
        self.puerto = 'COM3'

        # revisar a que puerto esta conectado el arduino
        puertos = serial.tools.list_ports.comports()
        for p in puertos:
            if "CH340" in p.description:
                print(p.device, p.description)
                self.puerto = p.device


        self.arduino = serial.Serial(self.puerto, 9600)
        time.sleep(2)  # Espera a que se estabilice la conexión

        # Temporizador para leer datos cada 200 ms
        self.timer = QTimer()
        self.comprobarFinalizacion = QTimer()
        self.timer.timeout.connect(self.leer_serial)
        # self.comprobarFinalizacion.timeout.connect(self.ajustarTiempoCero)
        self.timer.start(10)

        #recuperacion usuario y contraseña
        self.destinatario = ""
        self.codigo = []
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.sender_email = "tu_email_de_envio@gmail.com"
        self.usuario = "pepito5"
        self.contraseña = "1234"



    def creditos(self):
        print("Creditos ingresados:",self.ui.spinCreditos.value())
        creditos_cargados = "C" + str(self.ui.spinCreditos.value())
        self.creditos_boxes[self.actualBox] = self.ui.spinCreditos.value()
        # self.tiempo_boxes[self.actualBox] = self.creditos_boxes[self.actualBox] * self.tiempo_credito
        self.arduino.write(creditos_cargados.encode())

    def cambioBox(self, index):
        self.actualBox = index
        print(self.actualBox)

    def separar_num(self, tiempo):
        if ":" in tiempo:
            self.min = ""
            for i in tiempo:
                if i == ":":
                    break
                if tiempo.find(i) > 1:
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
    
    def imprimir_tiempo(self):
        min = str(self.tiempo_boxes[self.actualBox][0])
        sec = str(self.tiempo_boxes[self.actualBox][1])
        if self.tiempo_boxes[self.actualBox][1] < 10:
            sec = "0" + sec
        self.ui.lcdTime.display(f"{min}:{sec}")
    
    # def ajustarTiempoCero(self):
    #     self.ui.pushIniciar.setEnabled(True)
    #     self.comprobarFinalizacion.stop()


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
        print(tiempo_total, tiempo_consumido)
        self.ui.progressTime.setValue(porcentaje)
    
    def leer_serial(self):
        if self.arduino.in_waiting > 0:
            self.mensaje = self.arduino.readline().decode().strip()
            print(self.mensaje, self.tiempo_boxes)
            # if ":" in self.mensaje:
            #     self.ui.pushIniciar.setEnabled(False)
            #     self.tupla_tiempo = self.separar_num(self.mensaje)
            #     self.imprimir_tiempo()
            #     self.barra_porcentaje()
            #     if self.tupla_tiempo[1] == 1 and self.tupla_tiempo[0] == 0:
            #         self.comprobarFinalizacion.start(1000)
            if "T" in self.mensaje:
                indice = self.mensaje.find('T')
                box = self.mensaje[indice + 1]
                self.ui.pushIniciar.setEnabled(False)
                self.tupla_tiempo = self.separar_num(self.mensaje)
                self.tiempo_boxes[int(box)-1] = self.tupla_tiempo
                self.imprimir_tiempo()
                self.barra_porcentaje()
                if self.tupla_tiempo[1] == 1 and self.tupla_tiempo[0] == 0:
                    self.comprobarFinalizacion.start(1000)
     
            elif "A" in self.mensaje:
                self.ui.agua.setStyleSheet("background-color: lightgreen;") # <--
                self.ui.jabon.setStyleSheet("background-color: white;")
                self.ui.foam.setStyleSheet("background-color: white;")
                self.ui.desengrasante.setStyleSheet("background-color: white;")
                self.ui.cera.setStyleSheet("background-color: white;")
            elif "J" in self.mensaje:
                self.ui.agua.setStyleSheet("background-color: white;")
                self.ui.jabon.setStyleSheet("background-color: lightgreen;") # <--
                self.ui.foam.setStyleSheet("background-color: white;")
                self.ui.desengrasante.setStyleSheet("background-color: white;")
                self.ui.cera.setStyleSheet("background-color: white;")
            elif "D" in self.mensaje:
                self.ui.agua.setStyleSheet("background-color: white;")
                self.ui.jabon.setStyleSheet("background-color: white;") 
                self.ui.foam.setStyleSheet("background-color: white;")
                self.ui.desengrasante.setStyleSheet("background-color: lightgreen;") # <--
                self.ui.cera.setStyleSheet("background-color: white;")
            elif "F" in self.mensaje:
                self.ui.agua.setStyleSheet("background-color: white;")
                self.ui.jabon.setStyleSheet("background-color: white;") 
                self.ui.foam.setStyleSheet("background-color: lightgreen;") # <--
                self.ui.desengrasante.setStyleSheet("background-color: white;")
                self.ui.cera.setStyleSheet("background-color: white;")
            elif "C" in self.mensaje:
                self.ui.agua.setStyleSheet("background-color: white;")
                self.ui.jabon.setStyleSheet("background-color: white;") 
                self.ui.foam.setStyleSheet("background-color: white;")
                self.ui.desengrasante.setStyleSheet("background-color: white;")
                self.ui.cera.setStyleSheet("background-color: lightgreen;") # <--



    #Recuperar contraseña y usuario
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AquaManager Login")
        self.setGeometry(100, 100, 400, 200)
        
        # -----------------------------------------------------------
        # 🔑 ATRIBUTOS DE CONFIGURACIÓN Y CREDENCIALES (Ajustar Aquí)
        # -----------------------------------------------------------
        
        # Configuración del servidor de correo
        self.smtp_server = "smtp.gmail.com"  # O el servidor SMTP que uses
        self.port = 587
        self.sender_email = "soporte.aquamanager@gmail.com" 

        self.email_password = "TU_CONTRASEÑA_DE_ENVIO_SMTP" 
        
        # Credenciales que se enviarán al usuario (Simulación de la BD)
        self.usuario = "pepito5"
        self.contraseña = "1234"    
        
        # Variable para el destinatario (se llenará desde la interfaz)
        self.destinatario = ""
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz principal (simulada) y conecta los botones."""
        layout = QVBoxLayout()
        
        # Simulación de campos de login
        
        # Botón para activar el diálogo de recuperación
        self.recover_btn = QPushButton("Olvidé mi usuario/contraseña")
        self.recover_btn.clicked.connect(self.abrir_dialogo_recuperacion)
        layout.addWidget(self.recover_btn)
        
        self.setLayout(layout)

    # -----------------------------------------------------------
    # 🖼️ LÓGICA DE LA INTERFAZ QT
    # -----------------------------------------------------------

    def abrir_dialogo_recuperacion(self):
        """Abre un diálogo modal para solicitar el email del destinatario."""
        self.recovery_dialog = QDialog(self)
        self.recovery_dialog.setWindowTitle("Recuperación de Credenciales")
        
        layout = QVBoxLayout(self.recovery_dialog)
        layout.addWidget(QLabel("Ingresa el correo electrónico asociado a tu cuenta:"))
        
        # Campo de entrada para el email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ejemplo@correo.com")
        layout.addWidget(self.email_input)
        
        # Botón de envío
        self.send_btn = QPushButton("Enviar Credenciales")
        # Conecta el botón a la función que maneja la lógica
        self.send_btn.clicked.connect(self.manejar_solicitud_recuperacion)
        layout.addWidget(self.send_btn)
        
        self.recovery_dialog.exec_()
        
    def manejar_solicitud_recuperacion(self):
        """Recupera el email del campo, lo asigna a 'self.destinatario' e inicia el envío."""
        
        email_ingresado = self.email_input.text().strip()
        
        if not email_ingresado:
            QMessageBox.warning(self, "Error", "Por favor, ingresa un correo electrónico.")
            return

        # 1. Asignar el email del input a la variable de la clase
        self.destinatario = email_ingresado
        
        # 2. Iniciar el envío
        envio_exitoso = self.enviar_codigo_por_email()

        # 3. Mostrar feedback al usuario
        if envio_exitoso:
            QMessageBox.information(self, "Éxito", f"Tus credenciales han sido enviadas a {self.destinatario}. Revisa tu bandeja de entrada.")
            self.recovery_dialog.close()
        else:
            QMessageBox.critical(self, "Error de Envío", "No se pudo enviar el correo. Revisa los datos SMTP en el código y tu conexión.")
        
    # -----------------------------------------------------------
    # 📧 LÓGICA DE ENVÍO DE CORREO
    # -----------------------------------------------------------
    
    def enviar_codigo_por_email(self):
        """Envía el usuario y contraseña al destinatario."""
        
        # Prepara el mensaje
        asunto = "Credenciales de Acceso - AquaManager"
        cuerpo = f"""
        Hola,

        Al parecer olvidaste tu usuario y contraseña de ingreso a AquaManager
        ¡No te procupes, en este correo te lo facilitaremos!
        
        Usuario: {self.usuario}
        Contraseña: {self.contraseña}

        Atentamente,
        El Equipo de Soporte de AquaManager
        """

        msg = MIMEText(cuerpo, 'plain', 'utf-8')
        msg['Subject'] = Header(asunto, 'utf-8')
        msg['From'] = formataddr((str(Header('AquaManager Soporte', 'utf-8')), self.sender_email))
        msg['To'] = self.destinatario # Usa el email que el usuario ingresó
    
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls() # Inicia el cifrado TLS
                
                # AUTENTICACIÓN: Usa la contraseña de la cuenta de envío (SMTP App Password)
                server.login(self.sender_email, self.email_password) 
                
                server.sendmail(self.sender_email, self.destinatario, msg.as_string())
            return True
        except Exception as e:
            # Puedes usar print para debug, pero la QMessageBox en manejar_solicitud_recuperacion es para el usuario
            print(f"Error SMTP al enviar correo: {e}")
            return False

# -----------------------------------------------------------
# 🚀 EJECUCIÓN DEL PROGRAMA
# -----------------------------------------------------------

#if __name__ == '__main__':
#    # Asegúrate de que las librerías están disponibles.
#    try:
#        app = QApplication(sys.argv)
#        window = LoginApp()
#        window.show()
#        sys.exit(app.exec_())
#    except ImportError as e:
#        print("Faltan módulos. Asegúrate de instalar PyQt5, y las librerías de Python.")
#        print(f"Error: {e}")
    

    



# ------------------ MAIN PROGRAM ------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
