from flask import Flask, request, jsonify
from google.cloud import firestore

# Initialize Flask app
app = Flask(__name__)

# Conectar con Firestore
db = firestore.Client()

# Colección de incidentes en Firestore
INCIDENT_COLLECTION = 'incidentes'


# Ruta para crear un incidente
@app.route('/incidentes', methods=['POST'])
def create_incident():
    try:
        # Obtener el mensaje del cuerpo de la solicitud
        data = request.get_json()
        mensaje = data.get('mensaje')

        if not mensaje:
            return jsonify({'error': 'El mensaje es requerido'}), 400

        # Crear un nuevo incidente
        incidente_ref = db.collection(INCIDENT_COLLECTION).document()
        incidente_ref.set({
            'mensaje': mensaje
        })

        return jsonify({"id": incidente_ref.id, "mensaje": mensaje}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ruta para actualizar un incidente existente
@app.route('/incidentes/<string:id>', methods=['PUT'])
def update_incidente(id):
    try:
        # Obtener el mensaje del cuerpo de la solicitud
        data = request.get_json()
        mensaje = data.get('mensaje')

        if not mensaje:
            return jsonify({'error': 'El mensaje es requerido'}), 400

        # Referencia al documento de Firestore
        incidente_ref = db.collection(INCIDENT_COLLECTION).document(id)
        incidente = incidente_ref.get()

        if not incidente.exists:
            return jsonify({'error': 'Incidente no encontrado'}), 404

        # Actualizar el incidente
        incidente_ref.update({
            'mensaje': mensaje
        })

        return jsonify({"id": incidente_ref.id, "mensaje": mensaje}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
