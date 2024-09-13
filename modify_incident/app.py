from flask import Flask, request, jsonify, Response
from google.cloud import firestore

# Initialize Flask app
app = Flask(__name__)

# Conexion a Firestore
db = firestore.Client(database="incidentsdb")

# Nombre de la colección de incidentes
INCIDENT_COLLECTION = "incidents"

API_PREFIX = "/v1/incidents"


# Ruta para crear un incidente
@app.route(API_PREFIX, methods=["POST"])
def create_incident():
    try:
        # Obtener el mensaje del cuerpo de la solicitud
        data = request.get_json()
        mensaje = data.get("mensaje")

        if not mensaje:
            return jsonify({"error": "El mensaje es requerido"}), 400

        # Crear un nuevo incidente
        incidente_ref = db.collection(INCIDENT_COLLECTION).document()
        incidente_ref.set({"mensaje": mensaje})

        return jsonify({"id": incidente_ref.id, "mensaje": mensaje}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para actualizar un incidente existente
@app.route(f"{API_PREFIX}/<string:id>", methods=["PUT"])
def update_incidente(id):
    try:
        # Obtener el mensaje del cuerpo de la solicitud
        data = request.get_json()
        mensaje = data.get("mensaje")

        if not mensaje:
            return jsonify({"error": "El mensaje es requerido"}), 400

        # Referencia al documento de Firestore
        incidente_ref = db.collection(INCIDENT_COLLECTION).document(id)
        incidente = incidente_ref.get()

        if not incidente.exists:
            return jsonify({"error": "Incidente no encontrado"}), 404

        # Actualizar el incidente
        incidente_ref.update({"mensaje": mensaje})

        return jsonify({"id": incidente_ref.id, "mensaje": mensaje}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Health Check
@app.route("/ping")
def health_check():
    return Response("pong", status=200, mimetype="text/plain")


# Iniciar la aplicación
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
