from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message # Importamos las herramientas de correo

app = Flask(__name__)

# --- CONFIGURACIÓN DE CORREO ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'infiwebspa@gmail.com' # Tu correo
app.config['MAIL_PASSWORD'] = 'dpdu pflb fjzb jlor' # No es tu clave normal
app.config['MAIL_DEFAULT_SENDER'] = 'infiwebspa@gmail.com'

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message_content = data.get('message')

    try:
        # Creamos el objeto del mensaje
        msg = Message(
            subject=f"Nuevo mensaje de contacto de {name}",
            recipients=['infiwebspa.contactanos@gmail.com'], # A quién le llega
            body=f"Has recibido un nuevo mensaje:\n\nNombre: {name}\nCorreo: {email}\n\nMensaje:\n{message_content}"
        )
        
        # Enviamos el correo
        mail.send(msg)
        
        print(f"Correo enviado con éxito de parte de {name}")
        return jsonify({"success": True, "message": "Mensaje enviado correctamente"}), 200

    except Exception as e:
        print(f"Error enviando correo: {e}")
        return jsonify({"success": False, "message": "No se pudo enviar el correo"}), 500

if __name__ == '__main__':
    app.run(debug=False, port=8080, host="0.0.0.0")