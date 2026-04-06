from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    # Aquí puedes agregar lógica para enviar correo o guardar en DB
    print(f"Nuevo mensaje de {name} ({email}): {message}")
    return jsonify({"success": True, "message": "Mensaje enviado correctamente"}), 200

if __name__ == '__main__':
    app.run(debug=False, port=8080, host="0.0.0.0")