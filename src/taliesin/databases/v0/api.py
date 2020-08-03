import json
from typing import Any
from typing import Dict
from typing import List

from flask import Blueprint
from flask import request
from flask import Response
from taliesin.database import db_session
from taliesin.databases.v0.models import Database
from taliesin.databases.v0.schemas import DatabaseSchema
from taliesin.queries.v0.schemas import QuerySchema


blueprint = Blueprint("v0/databases", __name__, url_prefix="/api/v0/databases")

databases_schema = DatabaseSchema(many=True)
database_schema = DatabaseSchema()
query_schema = QuerySchema()


@blueprint.route("", methods=["GET"])
def get_databases() -> Response:
    databases: List[Database] = Database.query.all()
    payload: List[Dict[str, Any]] = databases_schema.dump(databases)
    return Response(json.dumps(payload), mimetype="application/json")


@blueprint.route("", methods=["POST"])
def post_databases() -> Response:
    database = database_schema.load(request.json)
    db_session.add(database)
    db_session.commit()
    payload = database_schema.dump(database)
    return Response(json.dumps(payload), mimetype="application/json", status=201)


@blueprint.route("/<database_name>/queries", methods=["POST"])
def post_queries(database_name: str) -> Response:
    database = Database.query.filter(Database.name == database_name).one()

    payload = request.json
    payload.setdefault("database_id", database.id)
    query = query_schema.load(payload)
    db_session.add(query)
    db_session.commit()

    query = database.connection.submit_query(query)
    db_session.commit()

    payload = query_schema.dump(query)
    return Response(json.dumps(payload), mimetype="application/json", status=201)
