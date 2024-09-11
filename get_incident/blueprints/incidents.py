from flask import Blueprint, Response, current_app, request
from flask.views import MethodView
from repositories import IncidentRepository
from .util import class_route

blp = Blueprint("Incident", __name__)


@class_route(blp, "/<id>")
class IncidentView(MethodView):
    init_every_request = False

    def get(self, id):
        Incident_repository = current_app.repositories[IncidentRepository]
        Incident = Incident_repository.get_incident(id)

        resp = Response(
            f"Incident: {Incident}\n\nHeaders:\n{request.headers}",
            status=200,
            mimetype="text/plain",
        )
        return resp
