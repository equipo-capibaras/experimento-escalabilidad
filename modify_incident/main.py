from flask import Flask, request, jsonify
from google.cloud import secretmanager
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Initialize Flask app
app = Flask(__name__)


# Credenciales de Firebase
def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(name=name)
    secret_payload = response.payload.data.decode("UTF-8")

    return secret_payload


# Obtener las credenciales desde Google Secret Manager
service_account_info = access_secret_version("FIREBASE_SERVICE_ACCOUNT")

# Colección de incidentes en Firestore
INCIDENT_COLLECTION = access_secret_version("FIRESTORE_COLLECTION_NAME")

# Conectar con Firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.Client()


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
