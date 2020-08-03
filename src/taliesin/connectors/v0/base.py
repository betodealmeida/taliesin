from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import cast

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

    def __init__(self, *args: Any, **kwargs: Any):
        pass

    @abstractmethod
    def submit_query(self, query: Query, **connector_kwargs: str) -> Query:
        raise NotImplementedError("Subclasses MUST implement submit_query")

    def get_query(self, query_id: str, **connector_kwargs: str) -> Query:
        return cast(Query, Query.query.filter(Query.id == query_id).one())
