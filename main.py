#main.py
from flask import Flask, jsonify, request
from funciones import enviar_correo, enviar_correo_autentificacion, enviar_correo_reset_password, enviar_correo_cambio_email
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=False)