import os
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import secretmanager
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()


app = Flask(__name__)


def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(name=name)
    secret_payload = response.payload.data.decode("UTF-8")

    return secret_payload


# Obtener las credenciales desde Google Secret Manager
service_account_info = access_secret_version("FIREBASE_SERVICE_ACCOUNT")

# Obtener el nombre de la colección desde Google Secret Manager
collection_name = access_secret_version("FIRESTORE_COLLECTION_NAME")

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.route("/incidents/<string:doc_id>", methods=["GET"])
def get_data(doc_id):
    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc = doc_ref.get()

        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "Documento no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
