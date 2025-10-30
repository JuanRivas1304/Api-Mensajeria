import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
import random 
import string
from jinja2 import Environment, FileSystemLoader

# Ruta al directorio actual (donde está funciones.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar plantillas desde carpeta templates_email
env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates_email')))

def enviar_correo(email_receiver):
    load_dotenv()

    email_sender = "juandiegomurillorivas2@gmail.com"
    password = os.getenv("PASSWORD")  # Asegúrarse de que PASSWORD esté configurado en el archivo .env
    
    subject = "Bienvenido a OdontoSalud"

    # Cargar plantilla HTML
    template = env.get_template("bienvenida.html")
    body = template.render()

    # Crear el mensaje de correo
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body, subtype='html')  # Establecer el contenido como HTML

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return f"Correo enviado exitosamente a {email_receiver}"

def generar_codigo_autentificacion():
    """Genera un codigo aleatorio de 6 digitos"""
    return ''.join(random.choices(string.digits, k=6))

def enviar_correo_autentificacion(email_receiver):
    load_dotenv()

    email_sender = "juandiegomurillorivas2@gmail.com"
    password = os.getenv("PASSWORD")

    #Genera el codigo de autentificacion
    codigo_autentificacion = generar_codigo_autentificacion()

    subject = "Codigo de Autentificacion"

    # Cargar plantilla HTML
    template = env.get_template("codigo_autentificacion.html")
    body = template.render(codigo_autentificacion=codigo_autentificacion)

    #Mensaje de correo
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return codigo_autentificacion

def enviar_correo_reset_password(email_receiver):
    load_dotenv()

    email_sender = "juandiegomurillorivas2@gmail.com"
    password = os.getenv("PASSWORD")

    #Genera el codigo de reestablecimiento
    codigo_autentificacion_reset_password = generar_codigo_autentificacion()

    subject = "Restablecimiento de Contraseña"

    # Cargar plantilla HTML
    template = env.get_template("reset_password.html")
    body = template.render(codigo=codigo_autentificacion_reset_password)

    # Crear el mensaje de correo
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return codigo_autentificacion_reset_password

def enviar_correo_cambio_email(old_email, new_email, username):
    load_dotenv()

    email_sender = "juandiegomurillorivas2@gmail.com"
    password = os.getenv("PASSWORD")

    subject = "Notificación de cambio de correo en OdontoSalud"

    # Usar plantilla personalizada (crear archivo luego)
    template = env.get_template("notificacion_cambio_email.html")
    body = template.render(username=username, new_email=new_email)

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = old_email
    em["Subject"] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, old_email, em.as_string())

    return True

def enviar_correo_nueva_cita(email_receiver, fecha_cita, hora_cita, doctor, servicio):
    """Enviar correo cuando un usuario reserva una cita"""
    load_dotenv()
    email_sender = "juandiegomurillorivas2@gmail.com"
    password = os.getenv("PASSWORD")

    subject = "Confirmación de cita en OdontoSalud"

    template = env.get_template("nueva_cita.html")
    body = template.render(
        fecha_cita=fecha_cita,
        hora_cita=hora_cita,
        doctor=doctor,
        servicio=servicio
    )

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return True


def enviar_correo_cambio_cita(email_receiver, fecha_anterior, hora_anterior, fecha_nueva, hora_nueva, doctor, servicio):
    """Enviar correo cuando un usuario cambia una cita"""
    load_dotenv()
    email_sender = "juandiegomurillorivas2@gmail.com"
    password = os.getenv("PASSWORD")

    subject = "Cambio de cita en OdontoSalud"

    template = env.get_template("cambio_cita.html")
    body = template.render(
        fecha_anterior=fecha_anterior,
        hora_anterior=hora_anterior,
        fecha_nueva=fecha_nueva,
        hora_nueva=hora_nueva,
        doctor=doctor,
        servicio=servicio
    )

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return True


def enviar_correo_cancelacion_cita(email_receiver, fecha_cita, hora_cita, doctor, servicio):
    """Enviar correo cuando un usuario cancela una cita"""
    load_dotenv()
    email_sender = "juandiegomurillorivas2@gmail.com"
    password = os.getenv("PASSWORD")

    subject = "Cancelación de cita en OdontoSalud"

    template = env.get_template("cancelacion_cita.html")
    body = template.render(
        fecha_cita=fecha_cita,
        hora_cita=hora_cita,
        doctor=doctor,
        servicio=servicio
    )

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return True
