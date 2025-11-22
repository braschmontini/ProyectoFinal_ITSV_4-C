import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

class recuperar_contrasenia:
    def __init__(self, usuario, contrasenia):
        self.SENDER_EMAIL = "soporte.aquamanager@gmail.com"  # ⬅️ TU EMAIL DE ENVÍO
        self.EMAIL_PASSWORD = "dyph ejym szim eznh" # ⬅️ TU CLAVE DE APLICACIÓN
        self.SMTP_SERVER = "smtp.gmail.com"
        self.PORT = 587
        self.usuario = usuario
        self.contraseña = contrasenia

    def enviar_credenciales_por_email(self, destinatario): # ¡Renombrada para claridad!
        """Envía el usuario y contraseña al destinatario."""
        
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
        msg['From'] = formataddr((str(Header('AquaManager Soporte', 'utf-8')), self.SENDER_EMAIL))
        msg['To'] = destinatario
    
        try:
            with smtplib.SMTP(self.SMTP_SERVER, self.PORT) as server:
                server.starttls() # Inicia el cifrado TLS
                server.login(self.SENDER_EMAIL, self.EMAIL_PASSWORD) 
                server.sendmail(self.SENDER_EMAIL, destinatario, msg.as_string())
            return True
        except Exception as e:
            print(f"Error SMTP al enviar correo: {e}")
            return False


    def main(self):
        """Ejecuta el flujo completo de la prueba: solicitar email, enviar, solicitar código y verificar."""
        print("--- 📧 PRUEBA DE ENVÍO Y VERIFICACIÓN SMTP ---")
        
        # 1. Solicitar la dirección de correo
        destinatario = input("Ingresa la dirección de correo para la prueba: ").strip()
        
        if not destinatario:
            print("Dirección de correo no válida. Terminando programa.")
            return
        
        # 2. Enviar el correo
        envio_exitoso = self.enviar_credenciales_por_email(destinatario)
        
        if not envio_exitoso:
            print("\nPrueba de envío fallida. No se puede continuar.")
            return
