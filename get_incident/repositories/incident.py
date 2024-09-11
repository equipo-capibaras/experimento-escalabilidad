# incident_repository.py
from google.cloud import firestore


class IncidentRepository:
    def __init__(self, db: firestore.Client, collection_name):
        self.db = db
        self.collection_name = collection_name

    def get_incident(self, incident_id: str):
        try:
            doc_ref = self.db.collection(self.collection_name).document(incident_id)
            doc = doc_ref.get()

            if doc.exists:
                return doc.to_dict()
            else:
                return None
        except Exception as e:
            print(f"Error al obtener el incidente: {str(e)}")
            return None
