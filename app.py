import os
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# 🔐 CONFIGURACIÓN GMAIL (Railway ENV)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

# 🔥 IMPORTANTE → evita que se quede pegado
app.config['MAIL_TIMEOUT'] = 10

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    print("🔥 Request recibido")

    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No hay datos"}), 400

    name = data.get('name')
    email = data.get('email')
    message_content = data.get('message')

    if not name or not email or not message_content:
        return jsonify({"success": False, "message": "Faltan datos"}), 400

    try:
        print("📧 Intentando enviar correo...")

        msg = Message(
            subject=f"Nuevo mensaje de {name}",
            recipients=['infiwebspa.contactanos@gmail.com'],
            body=f"""
Has recibido un mensaje desde tu web:

Nombre: {name}
Correo: {email}

Mensaje:
{message_content}
"""
        )

        mail.send(msg)

        print("✅ Correo enviado correctamente")

        return jsonify({
            "success": True,
            "message": "Mensaje enviado correctamente"
        }), 200

    except Exception as e:
        print(f"❌ Error enviando correo: {str(e)}")

        return jsonify({
            "success": False,
            "message": "Error al enviar correo"
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)