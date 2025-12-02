import sys #Se usa para cerrar el programa
import serial #Permite la comunicacion con arduino
import serial.tools.list_ports #Perte listar los puertos COM disponibles

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox #Importa widgets centrales de Qt
#QApplication: instancia principal que gestiona la aplicación Qt
#QMainWindow: clase base para ventanas con menús, barras, áreas centrales, etc
#QMessageBox: ventanas emergentes de advertencia, error, información, etc

from PySide6.QtCore import QTimer, Qt, QSize 
#QTimer: permite ejecutar funciones de forma periódica (intervalos en ms)
# Qt: contiene constantes globales (colores, modos, alineaciones, etc.)
# QSize: se usa para definir tamaños (por ejemplo, para escalar un GIF)

from PySide6.QtGui import QMovie #QMovie: clase para reproducir GIFs animados dentro de un QLabel
from PySide6 import QtCore #Importa el módulo completo QtCore.

from untitled_ui import Ui_LoginWindow #Importa la clase de Qt Designer para la pantalla de login
from ui import Ui_MainWindow #Importa la clase   por Qt Designer para la pantalla de la aplicacion
from recuperar_mail import RecuperarWindow #Importa la clase   por Qt Designer para la pantalla de recuperacion

# ------------------ LOGIN WINDOW ------------------
class LoginWindow(QMainWindow): #Inicia ventana de login y define variables
    def __init__(self):
        
        self.usuario = ["AquaManager", "1234"]

        super().__init__()
        self.ui = Ui_LoginWindow()# Carga la interfaz gráfica generada por Qt Designer para la ventana de login.
        self.ui.setupUi(self)# Inserta todos los widgets definidos en la interfaz dentro de esta ventana.

        self.ui.lineEdit.setStyleSheet("color: black; background-color: white;")
        self.ui.lineEdit_2.setStyleSheet("color: black; background-color: white;")
        self.ui.loginButton.setStyleSheet("color: black; background-color: white;")

    def recuperacion(self): #Ejecuta y abre la ventana de recuperacion de contraseña
        self.recuperar_window = RecuperarWindow(self.usuario[0], self.usuario[1])
        self.recuperar_window.show()

    def open_main_window(self): #Ejecuta y abre la interfaz del proyecto
        self.main_window = MainWindow(self.arduino, self.puerto)
        self.main_window.show()
        self.close()

    def checklogin(self):
        username = self.ui.lineEdit.text()   #Comparan los usuarios y contraseñas
        password = self.ui.lineEdit_2.text() #

        if username == self.usuario[0] and password == self.usuario[1]: #Si son correctos inicia el GIF de carga
            gif = QMovie("GIF_Carga.gif")
            gif.setScaledSize(QSize(85, 85))
            self.ui.GIFdeCarga.setMovie(gif)
            gif.start()
            try:
                # revisar a que puerto esta conectado el arduino
                puertos = serial.tools.list_ports.comports()
                for p in puertos:
                    if "CH340" in p.description:
                        self.puerto = p.device
                        
                
                self.arduino = serial.Serial(self.puerto, 9600)
                QtCore.QTimer.singleShot(5000, self.open_main_window)

            except: #Errores por si no hay nada conectado
                print("ERROR: puerto al arduino no localizado. Por favor verifique la conexion.")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText("Puerto no detectado, conecte el arduino")
                msg.setStyleSheet("QMessageBox { background-color: white; }")
                msg.exec()
                gif.stop()
                self.ui.GIFdeCarga.clear()   # borra el contenido sin colapsar el QLabel
            
        else: #Alerta si los usuarios y contraseñas son equivocados
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Usuario o contraseña incorrectos")
            msg.setStyleSheet("QMessageBox { background-color: white; }")
            msg.exec()



# ------------------ MAIN WINDOW ------------------
class MainWindow(QMainWindow):  #Clase MainWindow heredada de QMainWindow, que es una clase de PyQt para crear la ventana principal de la app.
    def __init__(self, arduino = None, puerto = None): #constructor method. Se ejuecuta cuando la instancia de la clase es creada.
        super().__init__() #llama al constructor de la clase QMainWindow, para inicializar las funcionalidades básicas de la ventana principal de la app.
        self.ui = Ui_MainWindow() #crea una instancia de Ui_MainWindow class, la cual es la definición de la interfaz del usuario para la ventana principal.
        self.ui.setupUi(self) #llama al método setupUi() de la instancia Ui_MainWindow, para setear los componenetes de la interfaz del usuario dentro de main window.

        self.tiempo_credito = 10

        self.creditos_boxes = []
        self.estado_boxes = [] # 0 es sin conexion, 1 es encendida, 2 es apagada
        self.tiempo_boxes = []
        self.productos = []
        for i in range(5):
            self.creditos_boxes.append(0)
            self.tiempo_boxes.append((0,0))
            self.productos.append("")
            self.estado_boxes.append(0)

        self.actualBox = 0 # 0 es 1, 1 es 2, etc...
        self.ui.listBox.addItems(["BOX 1", "BOX 2", "BOX 3", "BOX 4", "BOX 5"])

        self.arduino = arduino
        self.puerto = puerto

        tiempo_por_cred = f"T{self.tiempo_credito}\n"
        if self.arduino != None:
            self.arduino.write(tiempo_por_cred.encode())

        self.timer = QTimer() #Inicia el temporizador
        self.estado = QTimer() #inicializa la variable 
        self.timer.timeout.connect(self.leer_serial)
        self.estado.timeout.connect(self.actualizar_estados)
        if self.arduino != None: #Compara si arduino es diferente a None
            self.timer.start(10)
            self.estado.start(100)

    def creditos(self): #Toma la cant. de creditos dados, lo almacena en una box y envia C5\n por ej
        creditos_cargados = "C" + str(self.ui.spinCreditos.value()) + "\n"
        self.creditos_boxes[self.actualBox] = self.ui.spinCreditos.value()
        self.arduino.write(creditos_cargados.encode())
    
    def cambio_box_lista(self, indice): #Cambia el box activo al seleccionado en la lista.
        self.actualBox = indice

    def separar_num(self, tiempo): #recibe un tiempo, lo separa en seg y min y returna una tupla
        if "T" in tiempo:
            box_tiempo = tiempo.split("T") #Separa
            min_sec = box_tiempo[1].split(":") #Separa
            return int(min_sec[0]), int(min_sec[1]) #Crea tupla
    
    def imprimir_tiempo(self): #Toma el tiempo del box actual lo imprime en mm:ss lo muestra en el LCD
        min = str(self.tiempo_boxes[self.actualBox][0])
        sec = str(self.tiempo_boxes[self.actualBox][1])
        if self.tiempo_boxes[self.actualBox][1] < 10:
            sec = "0" + sec
        self.ui.lcdTime.display(f"{min}:{sec}")
    
    def imprimir_producto(self): #Setea los botones a blanco
        self.ui.agua.setStyleSheet("background-color: white;")
        self.ui.jabon.setStyleSheet("background-color: white;")
        self.ui.foam.setStyleSheet("background-color: white;")
        self.ui.desengrasante.setStyleSheet("background-color: white;")
        self.ui.cera.setStyleSheet("background-color: white;")
            #Los pone de color verde si hay cambios
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

    def barra_porcentaje(self): #Calcula el porcentaje y lo actualiza
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

    def actualizar_estados_interfaz(self): #Colore los boxes segun estado
        for i in range(5):
            if self.estado_boxes[i] == 0:
                self.ui.listBox.item(i).setForeground(Qt.GlobalColor.lightGray)
            elif self.estado_boxes[i] == 2:
                self.ui.listBox.item(i).setForeground(Qt.GlobalColor.red)
            elif self.estado_boxes[i] == 1:
                self.ui.listBox.item(i).setForeground(Qt.GlobalColor.green)
    
    def leer_serial(self):
        try:
            if self.arduino.in_waiting > 0:  # Verifica si hay datos disponibles para leer desde el puerto serie.
                self.mensaje = self.arduino.readline().decode().strip()  # Lee una línea completa enviada por Arduino, la decodifica y elimina espacios/saltos extra.
                box = int(self.mensaje[0]) - 1 # El primer carácter del mensaje indica el número de box (1–5). Se convierte a índice (0–4).
                if self.estado_boxes[box] == 0:  # Si el estado del box está como "sin conexión" (0), pero llegó un mensaje, lo cambia a estado "activo/encendido" (1).
                    self.estado_boxes[box] = 1

                if "T" in self.mensaje:  # Si el mensaje contiene "T", significa que trae tiempo del tipo "T02:30".
                    self.tiempo_boxes[box] = self.separar_num(self.mensaje) # Convierte el string "Tmm:ss" en una tupla (mm, ss) y lo guarda
                        
                elif "A" in self.mensaje:# Si contiene "A", "J", "D", "F" o "C", asigna el producto seleccionado para ese box.
                    self.productos[box] = 'A'
                elif "J" in self.mensaje:
                    self.productos[box] = 'J'
                elif "D" in self.mensaje:
                    self.productos[box] = 'D'
                elif "F" in self.mensaje:
                    self.productos[box] = 'F'
                elif "C" in self.mensaje:
                    self.productos[box] = 'C'

                # Actualiza la interfaz gráfica con el producto, tiempo y barra de progreso.
                self.imprimir_producto()
                self.imprimir_tiempo()
                self.barra_porcentaje()

                #---- Definir estado de cada box ----

                for i in range(5):
                    if self.tiempo_boxes[i] == (0, 0):
                        self.estado_boxes[i] = 0

                if "off" in self.mensaje:
                    self.estado_boxes[box] = 2
                elif self.tiempo_boxes[box] != (0, 0):
                    self.estado_boxes[box] = 1

                 # ----- CONTROL DE VISIBILIDAD Y PERMISOS EN LA INTERFAZ -----

                # Si el tiempo llegó a cero y el estado es "apagado" → habilita botón "Iniciar" y oculta los grupos de opciones.
                if self.tiempo_boxes[self.actualBox] == (0, 0) and self.estado_boxes[self.actualBox] == 2:
                    self.ui.pushIniciar.setEnabled(True)
                    self.ui.groupTimer.hide()
                    self.ui.groupWashOptions.hide()

                # Si el estado es "sin conexión":
                elif self.estado_boxes[self.actualBox] == 0:
                    self.ui.pushIniciar.setEnabled(False)
                    self.ui.groupTimer.hide()
                    self.ui.groupWashOptions.hide()
                    
                else:# Si está activo:
                    self.ui.pushIniciar.setEnabled(False)
                    self.ui.groupTimer.show()
                    self.ui.groupWashOptions.show()
        except:# Si hubo cualquier error leyendo el puerto serie, se informa la posible pérdida de conexión.
            print("Se ha perdidio la conexion a arduino.")

    def actualizar_estados(self): #Envía el comando "?\n" a Arduino, permite consultar estados cada 100 ms.
        self.arduino.write(b'?\n')


# ------------------ MAIN PROGRAM ------------------
if __name__ == "__main__": #Crea la aplicacion Qt, muestra el Login y ejecuta el ciclo del programa
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())