from flask import Flask
from blueprints import BlueprintHealth, BlueprintIncidents
from repositories import IncidentRepository
from google.cloud import firestore

API_PREFIX = "/v1/incidents"


def create_app():
    app = Flask(__name__)

    try:
        collection_name = "incidents"
    except Exception as e:
        print(f"Error al obtener el nombre de la colección: {e}", flush=True)
        raise

    try:
        db = firestore.Client()
    except Exception as e:
        print(f"Error al inicializar Firestore: {e}", flush=True)
        raise

    app.repositories = {IncidentRepository: IncidentRepository(db, collection_name)}

    app.register_blueprint(BlueprintHealth)
    app.register_blueprint(BlueprintIncidents, url_prefix=API_PREFIX)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=8080, debug=True)
