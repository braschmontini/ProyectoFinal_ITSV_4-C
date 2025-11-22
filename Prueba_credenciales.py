import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# =========================================================
# 🛑 PASO 1: CONFIGURACIÓN SMTP (¡DEBES MODIFICAR ESTO!)
# =========================================================
SENDER_EMAIL = "soporte.aquamanager@gmail.com"  # ⬅️ TU EMAIL DE ENVÍO
EMAIL_PASSWORD = "dyph ejym szim eznh" # ⬅️ TU CLAVE DE APLICACIÓN
SMTP_SERVER = "smtp.gmail.com"
PORT = 587
# =========================================================


def generar_codigo():
    """Genera un código numérico aleatorio de 5 dígitos."""
    # Números entre 10000 y 99999
    return str(random.randint(10000, 99999))


def enviar_codigo(destinatario, codigo):
    """Establece la conexión SMTP y envía el correo con el código."""
    
    asunto = "Tu Código de Verificación"
    cuerpo = f"""
    Hola,

    Has solicitado un código de prueba. 
    
    Tu código numérico es: {codigo}

    Ingresa este código en la terminal para continuar.

    Saludos,
    Prueba SMTP
    """
    
    msg = MIMEText(cuerpo, 'plain', 'utf-8')
    msg['Subject'] = Header(asunto, 'utf-8')
    msg['From'] = formataddr((str(Header('Prueba SMTP', 'utf-8')), SENDER_EMAIL))
    msg['To'] = destinatario

    try:
        print(f"\nIntentando conectar con {SMTP_SERVER}:{PORT}...")
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls() # Inicia el cifrado TLS
            server.login(SENDER_EMAIL, EMAIL_PASSWORD) 
            server.sendmail(SENDER_EMAIL, destinatario, msg.as_string())
        
        print("✅ Correo enviado con éxito.")
        return True
    
    except Exception as e:
        print("\n❌ ERROR: No se pudo enviar el correo.")
        print(f"Detalle: {e}")
        print("Asegúrate de que SENDER_EMAIL y EMAIL_PASSWORD son correctos (usa una clave de aplicación si usas Gmail).")
        return False


def main():
    """Ejecuta el flujo completo de la prueba: solicitar email, enviar, solicitar código y verificar."""
    print("--- 📧 PRUEBA DE ENVÍO Y VERIFICACIÓN SMTP ---")
    
    # 1. Solicitar la dirección de correo
    destinatario = input("Ingresa la dirección de correo para la prueba: ").strip()
    
    if not destinatario:
        print("Dirección de correo no válida. Terminando programa.")
        return

    # 2. Generar el código secreto
    codigo_secreto = generar_codigo()
    
    # 3. Enviar el correo
    envio_exitoso = enviar_codigo(destinatario, codigo_secreto)
    
    if not envio_exitoso:
        print("\nPrueba de envío fallida. No se puede continuar.")
        return

    # 4. Solicitar al usuario que ingrese el código
    print("\n--- 📝 VERIFICACIÓN ---")
    print(f"El código secreto generado es: {codigo_secreto}") # Mostramos el código para la prueba simple
    
    codigo_ingresado = input("Introduce el código numérico que recibiste en tu email: ").strip()
    
    # 5. Comparar y dar resultado
    if codigo_ingresado == codigo_secreto:
        print("\n✨ **¡EXCELENTE!** El código es correcto. La prueba fue un éxito.")
    else:
        print("\n❌ Código incorrecto. Vuelve a intentar la prueba.")


if __name__ == "__main__":
    main()