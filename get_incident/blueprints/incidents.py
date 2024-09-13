from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from repositories import IncidentRepository
from .util import class_route

blp = Blueprint("Incident", __name__)


@class_route(blp, "/<id>")
class IncidentView(MethodView):
    init_every_request = False

    def get(self, id):
        Incident_repository = current_app.repositories[IncidentRepository]
        incident = Incident_repository.get_incident(id)

        return jsonify(incident), 200
