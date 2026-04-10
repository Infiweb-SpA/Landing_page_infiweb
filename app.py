import os
import threading
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# CONFIG GMAIL
app.config['MAIL_SERVER'] = '74.125.142.108'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
#app.config['MAIL_TIMEOUT'] = 10
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

# 🔥 FUNCIÓN QUE ENVÍA EL CORREO EN SEGUNDO PLANO
def send_email_async(app, msg):
    with app.app_context():
        try:
            print("📧 Enviando correo en background...")
            mail.send(msg)
            print("✅ Correo enviado")
        except Exception as e:
            print(f"❌ Error enviando correo: {e}")

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()

    if not data:
        return jsonify({"success": False}), 400

    name = data.get('name')
    email = data.get('email')
    message_content = data.get('message')

    if not name or not email or not message_content:
        return jsonify({"success": False}), 400

    msg = Message(
        subject=f"Nuevo mensaje de {name}",
        recipients=['infiwebspa@gmail.com'],
        body=f"""
Nombre: {name}
Correo: {email}

Mensaje:
{message_content}
"""
    )

    # 🚀 LANZAMOS EL ENVÍO EN BACKGROUND
    threading.Thread(target=send_email_async, args=(app, msg)).start()

    # 🔥 RESPONDEMOS INMEDIATAMENTE (NO SE CUELGA)
    return jsonify({
        "success": True,
        "message": "Mensaje enviado (procesando...)"
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
