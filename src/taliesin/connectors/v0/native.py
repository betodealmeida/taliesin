from datetime import datetime
from datetime import timezone

import apsw
from taliesin.connectors.v0.base import BaseConnector
from taliesin.queries.v0.models import Query


def row_factory(cursor, row):
    return {k[0]: row[i] for i, k in enumerate(cursor.getdescription())}


class NativeConnector(BaseConnector):

    name = "native"
    parameters = {
        "$schema": "https://json-schema.org/schema#",
        "$id": "https://github.com/betodealmeida/taliesin/jsonschema/connector/native.json",
        "title": "Native connector",
        "description": "Configuration for a native connector",
        "type": "object",
        "required": ["path"],
        "properties": {
            "path": {
                "type": "string",
                "title": "Path to a SQLite database",
                "default": ":memory:",
            },
        },
    }

    def __init__(self, path):
        self.connection = apsw.Connection(path)
        self.connection.setrowtrace(row_factory)

    def submit_query(self, query: Query, **connector_kwargs: str) -> Query:
        query.scheduled = datetime.now(timezone.utc)
        cursor = self.connection.cursor()

        query.started = datetime.now(timezone.utc)
        query.executed_query = query.submitted_query
        query.results = list(cursor.execute(query.executed_query))
        query.ended = datetime.now(timezone.utc)

        return query
