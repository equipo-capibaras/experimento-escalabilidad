import os
from flask import Flask
from blueprints import BlueprintHealth, BlueprintIncidents
from repositories import IncidentRepository
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import secretmanager
from dotenv import load_dotenv
import json

API_PREFIX = "/v1/incidents"

load_dotenv("../.env")


def access_secret_version(secret_id, version_id="latest"):
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

        if not project_id:
            raise EnvironmentError("GOOGLE_CLOUD_PROJECT no está configurado.")

        print(f"project_id: {project_id}", flush=True)

        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

        response = client.access_secret_version(name=name)
        secret_payload = response.payload.data.decode("UTF-8")
        return secret_payload
    except Exception as e:
        print(f"Error al acceder al secreto {secret_id}: {e}", flush=True)
        raise


def create_app():
    app = Flask(__name__)

    try:
        service_account_info = access_secret_version("firebase_service_account")
        service_account_info = json.loads(service_account_info)
    except Exception as e:
        print(f"Error al obtener credenciales de Firebase: {e}", flush=True)
        raise

    try:
        collection_name = access_secret_version("firestore_collection_name")
    except Exception as e:
        print(f"Error al obtener el nombre de la colección: {e}", flush=True)
        raise

    try:
        cred = credentials.Certificate(service_account_info)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error al inicializar Firebase: {e}", flush=True)
        raise

    db = firestore.client()

    app.repositories = {IncidentRepository: IncidentRepository(db, collection_name)}

    app.register_blueprint(BlueprintHealth)
    app.register_blueprint(BlueprintIncidents, url_prefix=API_PREFIX)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=8080, debug=True)
