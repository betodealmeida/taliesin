import json
from typing import Any
from typing import Dict
from typing import List

from flask import Blueprint
from flask import Response
from pkg_resources import iter_entry_points
from taliesin.connectors.v0.base import BaseConnector


blueprint = Blueprint("v0/connectors", __name__, url_prefix="/api/v0/connectors")


@blueprint.route("", methods=["GET"])
def connectors() -> Response:
    connectors: List[BaseConnector] = [
        entry_point.load() for entry_point in iter_entry_points("taliesin.connector")
    ]
    payload: List[Dict[str, Any]] = [
        {"name": connector.name, "parameters": connector.parameters}
        for connector in connectors
    ]
    return Response(json.dumps(payload), mimetype="application/json")
