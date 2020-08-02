import json
from typing import Any
from typing import Dict
from typing import List

from flask import Blueprint
from flask import jsonify
from flask import Response
from taliesin.databases.v0.models import Database
from taliesin.databases.v0.schemas import DatabaseSchema


blueprint = Blueprint("v0/databases", __name__, url_prefix="/api/v0/databases")

schema = DatabaseSchema(many=True)


@blueprint.route("", methods=["GET"])
def databases() -> Response:
    databases: List[Database] = Database.query.all()
    payload: Dict[str, Any] = schema.dump(databases)
    return Response(json.dumps(payload), mimetype="application/json")
