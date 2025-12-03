import smtplib #para conectarse a un servidor SMTP (como Gmail) y enviar mails.
from email.mime.text import MIMEText #para crear correos con contenido de texto.
from email.header import Header #para codificar correctamente cadenas como el título o el nombre del remitente.
from email.utils import formataddr # para mostrar el remitente como "Soporte AquaManager <correo@mail.com>".

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox #Importa PySide6 para manejar la interfaz gráfica Qt.
from PySide6.QtCore import Qt
from recuperacion import Ui_RecuperarContrasea #Importa la interfaz visual creada en Qt Designer (Ui_RecuperarContrasea).



class RecuperarWindow(QMainWindow):
    def __init__(self, usuario, contrasenia):
        super().__init__() #Inicia la ventana y carga su interfaz.
        self.ui = Ui_RecuperarContrasea()
        self.ui.setupUi(self)
        self.setWindowTitle("Recuperar Usuario")
        self.SENDER_EMAIL = "soporte.aquamanager@gmail.com"
        self.EMAIL_PASSWORD = "dyph ejym szim eznh"
        self.SMTP_SERVER = "smtp.gmail.com"
        self.PORT = 587
        self.usuario = usuario
        self.contraseña = contrasenia

    def enviar_credenciales_por_email(self, destinatario): #Envía el usuario y contraseña al destinatario. Retorna True si funciona
        asunto = "Credenciales de Acceso - AquaManager"
        cuerpo = f"""
        Hola,

        Al parecer olvidaste tu usuario y contraseña de ingreso a AquaManager.
        ¡No te preocupes, en este correo te lo facilitaremos!
        
        Usuario: {self.usuario}
        Contraseña: {self.contraseña}

        Atentamente,
        El Equipo de Soporte de AquaManager
        """

        msg = MIMEText(cuerpo, 'plain', 'utf-8') # Se arma el cuerpo del mensaje con los datos del usuario.
        msg['Subject'] = Header(asunto, 'utf-8')
        msg['From'] = formataddr((str(Header('AquaManager Soporte', 'utf-8')), self.SENDER_EMAIL))
        msg['To'] = destinatario
    
        try: #Conecta al servidor SMTP de Gmail -> Activa seguridad TLS -> Hace login con correo y App Password -> Envía el correo al destinatario.
            with smtplib.SMTP(self.SMTP_SERVER, self.PORT) as server:
                server.starttls()
                server.login(self.SENDER_EMAIL, self.EMAIL_PASSWORD)
                server.sendmail(self.SENDER_EMAIL, destinatario, msg.as_string())
            return True
        except Exception as e:
            print(f"Error SMTP al enviar correo: {e}")
            return False

    def mostrar_mensaje(self, titulo, texto, tipo="info"): #Función personalizada para mostrar mensajes con FONDO BLANCO y TEXTO LEGIBLE.

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(texto)
        
        if tipo == "error":
            msg_box.setIcon(QMessageBox.Critical)
        elif tipo == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setIcon(QMessageBox.Information)
        # Forzamos fondo blanco en la ventana, y fondo transparente en el texto
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: black;             /* Texto negro */
                background-color: transparent; /* Fondo transparente (para que se vea el blanco de atrás) */
            }
            /* Opcional: Estilo para que el botón también se vea bien */
            QMessageBox QPushButton {
                background-color: #0078d7; /* Azul estándar */
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #005a9e; /* Azul más oscuro al pasar el mouse */
            }
        """)
        
        msg_box.exec()

    def enviarmail(self):
        destinatario = self.ui.lineEdit.text().strip()
        
        if not destinatario: #Si esta vacio solicita una direccion 
            self.mostrar_mensaje("Atención", "Por favor, ingresa una dirección de correo válida.", "warning")
            return
        
        QApplication.setOverrideCursor(Qt.WaitCursor) #Muestra cursor de "cargando" mientras se envía el correo.
        envio_exitoso = self.enviar_credenciales_por_email(destinatario)
        QApplication.restoreOverrideCursor()

        if envio_exitoso: #Si funciona ejecuta una pestaña con este texto:
            self.mostrar_mensaje(
                "Envío Exitoso", 
                "El correo con tus credenciales ha sido enviado correctamente.\nRevisa tu bandeja de entrada.", 
                "info"
            )
            self.close() # Cierra la ventana
        else: #Si no funciona ejecuta una pestaña con este texto:
            self.mostrar_mensaje(
                "Error de Envío", 
                "No se pudo enviar el correo. \nVerifica tu conexión a internet o que la dirección sea correcta.", 
                "error"
            )