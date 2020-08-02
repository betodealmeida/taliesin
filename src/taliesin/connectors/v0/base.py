from abc import ABC
from abc import abstractmethod

from taliesin.queries.v0.models import Query


class BaseConnector(ABC):

    name = "base"
    parameters = {
        "$schema": "https://json-schema.org/schema#",
        "$id": "https://github.com/betodealmeida/taliesin/jsonschema/connector/base.json",
        "name": name,
        "title": "Base connector",
        "description": "Example configuration for a base connector",
        "type": "object",
        "required": [],
        "properties": {},
    }

    @abstractmethod
    def submit_query(self, query: Query, **connector_kwargs: str) -> Query:
        raise NotImplementedError("Subclasses MUST implement submit_query")

    @abstractmethod
    def get_query(self, query_id: str, **connector_kwargs: str) -> Query:
        raise NotImplementedError("Subclasses MUST implement get_query")
