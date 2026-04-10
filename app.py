import os
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# --- CONFIGURACIÓN DE CORREO SEGURA (USANDO VARIABLES DE RAILWAY) ---
# Estas variables se configuran en el panel de Railway, no se escriben aquí.
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

# Inicialización de Flask-Mail
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    # Obtenemos los datos enviados por el script.js
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message_content = data.get('message')

    # Verificación básica de datos
    if not name or not email or not message_content:
        return jsonify({"success": False, "message": "Faltan datos en el formulario"}), 400

    try:
        # Creamos el objeto del mensaje que recibirás en tu bandeja
        msg = Message(
            subject=f"Nuevo mensaje de contacto de {name}",
            recipients=['infiwebspa.contactanos@gmail.com'],
            body=f"Has recibido un nuevo mensaje desde la web:\n\n"
                 f"Nombre: {name}\n"
                 f"Correo del remitente: {email}\n\n"
                 f"Mensaje:\n{message_content}"
        )
        
        # Enviamos el correo a través del servidor de Google
        mail.send(msg)
        
        print(f"Correo enviado con éxito de parte de {name}")
        return jsonify({"success": True, "message": "Mensaje enviado correctamente"}), 200

    except Exception as e:
        # Si algo falla (como la clave de Gmail), lo veremos en los logs de Railway
        print(f"Error enviando correo: {str(e)}")
        return jsonify({"success": False, "message": "Error interno al enviar el correo"}), 500

if __name__ == '__main__':
    # Railway requiere que el puerto sea dinámico para poder conectar con internet
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)