import os
import resend
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configura tu API Key de Resend (Mejor si la pones en las variables de Railway)
resend.api_key = os.environ.get("RESEND_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No se recibieron datos"}), 400

    name = data.get('name')
    email = data.get('email')
    message_content = data.get('message')

    try:
        # Enviamos el correo usando la API de Resend
        params = {
            "from": "onboarding@resend.dev",
            "to": "infiwebspa@gmail.com", # El correo donde quieres recibir avisos
            "subject": f"Nuevo mensaje web de {name}",
            "html": f"""
                <h3>Nuevo mensaje de contacto</h3>
                <p><strong>Nombre:</strong> {name}</p>
                <p><strong>Email del cliente:</strong> {email}</p>
                <p><strong>Mensaje:</strong></p>
                <p>{message_content}</p>
            """
        }

        email_response = resend.Emails.send(params)
        print(f"✅ Correo enviado vía API: {email_response}")
        
        return jsonify({"success": True, "message": "¡Mensaje enviado con éxito!"}), 200

    except Exception as e:
        print(f"❌ Error con Resend: {e}")
        return jsonify({"success": False, "message": "Error interno al enviar"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
