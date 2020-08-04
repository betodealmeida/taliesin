import json
from typing import Any
from typing import Dict
from typing import List
from typing import Type

from flask import Blueprint
from flask import Response
from pkg_resources import iter_entry_points
from taliesin.connectors.v0.base import BaseConnector
from taliesin.connectors.v0.helpers import load_connectors


blueprint = Blueprint("v0/connectors", __name__, url_prefix="/api/v0/connectors")


@blueprint.route("", methods=["GET"])
def get_connectors() -> Response:
    connectors: List[Type[BaseConnector]] = list(load_connectors().values())
    payload: List[Dict[str, Any]] = [
        {"name": connector.name, "parameters": connector.parameters}
        for connector in connectors
    ]
    return Response(json.dumps(payload), mimetype="application/json")
