from taliesin.connectors.v0.base import BaseConnector
from taliesin.queries.v0.models import Query


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
        self.path = path

    def submit_query(self, query: Query, **connector_kwargs: str) -> Query:
        pass

    def get_query(self, query_id: str, **connector_kwargs: str) -> Query:
        pass
