#main.py
from flask import Flask, jsonify, request
from funciones import enviar_correo, enviar_correo_autentificacion, enviar_correo_reset_password, enviar_correo_cambio_email, enviar_correo_nueva_cita,enviar_correo_cambio_cita, enviar_correo_cancelacion_cita
from flask_cors import CORS 


app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return "root"

#Correo de bienvenida
@app.route('/enviar_correo', methods=['POST']) #en postman se coloca email_receiver=uncorreoreal@gmail.com
def llamar_enviar_correo():
    email_receiver = None 
    if request.is_json:
        email_receiver = request.json.get('email_receiver')
    else:
        email_receiver = request.args.get('email_receiver')

    if not email_receiver:
        return jsonify({'error': 'El parámetro email_receiver es requerido'}), 400

    resultado = enviar_correo(email_receiver)

    return jsonify({'mensaje': resultado})

#Correo de código de autentificación
@app.route('/codigo', methods=['POST']) #en postman se coloca email=uncorreoreal@gmail.com
def envio_codigo():
    #obtener el correo del usuario
    print(request.json)
    email = request.json.get('email')

    if not email:
        return jsonify({'error': 'El correo es necesario'}),400
    
    #enviar el codigo al correo del usuario
    codigo_autentificacion = enviar_correo_autentificacion(email)

    return jsonify({'mensaje': 'Correo enviado correctamente', 'codigo': codigo_autentificacion})

#Correo de reestablecimiento de contraseña
@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.json.get('email')

    if not email:
        return jsonify({'error': 'El correo es necesario'}), 400

    # Generar código y enviarlo con plantilla de reset password
    codigo = enviar_correo_reset_password(email)

    return jsonify({'mensaje': f'Código enviado a {email}', 'codigo': codigo})

#Notificacion por cambio de correo
@app.route('/notificar-cambio', methods=['POST'])
def notificar_cambio_correo():
    data = request.get_json()

    print("datos recibidos", data)
    old_email = data.get('old_email')
    new_email = data.get('new_email')
    username = data.get('username')
    
    if not old_email or not new_email or not username:
        return jsonify({'error': 'Faltan campos requeridos (oldEmail, newEmail, username)'}), 400

    try:
        enviar_correo_cambio_email(old_email, new_email, username)
        return jsonify({'mensaje': f'Correo de notificación enviado a {old_email}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Correo de confirmación de nueva cita
@app.route('/nueva-cita', methods=['POST'])
def correo_nueva_cita():
    data = request.get_json()
    email = data.get('email')
    fecha_cita = data.get('fecha_cita')
    hora_cita = data.get('hora_cita')
    doctor = data.get('doctor')
    servicio = data.get('servicio')

    if not all([email, fecha_cita, hora_cita, doctor, servicio]):
        return jsonify({'error': 'Faltan datos para enviar el correo de cita'}), 400

    try:
        enviar_correo_nueva_cita(email, fecha_cita, hora_cita, doctor, servicio)
        return jsonify({'mensaje': f'Correo de confirmación enviado a {email}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Correo por cambio de cita
@app.route('/cambio-cita', methods=['POST'])
def correo_cambio_cita():
    data = request.get_json()
    email = data.get('email')
    fecha_anterior = data.get('fecha_anterior')
    hora_anterior = data.get('hora_anterior')
    fecha_nueva = data.get('fecha_nueva')
    hora_nueva = data.get('hora_nueva')
    doctor = data.get('doctor')
    servicio = data.get('servicio')

    if not all([email, fecha_anterior, hora_anterior, fecha_nueva, hora_nueva, doctor, servicio]):
        return jsonify({'error': 'Faltan datos para el correo de cambio de cita'}), 400

    try:
        enviar_correo_cambio_cita(email, fecha_anterior, hora_anterior, fecha_nueva, hora_nueva, doctor, servicio)
        return jsonify({'mensaje': f'Correo de cambio de cita enviado a {email}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Correo por cancelación de cita
@app.route('/cancelacion-cita', methods=['POST'])
def correo_cancelacion_cita():
    data = request.get_json()
    email = data.get('email')
    fecha_cita = data.get('fecha_cita')
    hora_cita = data.get('hora_cita')
    doctor = data.get('doctor')
    servicio = data.get('servicio')

    if not all([email, fecha_cita, hora_cita, doctor, servicio]):
        return jsonify({'error': 'Faltan datos para el correo de cancelación'}), 400

    try:
        enviar_correo_cancelacion_cita(email, fecha_cita, hora_cita, doctor, servicio)
        return jsonify({'mensaje': f'Correo de cancelación enviado a {email}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=False)