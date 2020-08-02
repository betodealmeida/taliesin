from typing import Any
from typing import Dict

from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema
from taliesin.connectors.v0.schemas import ConnectorSchema
from taliesin.databases.v0.models import Database


class DatabaseSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    connector = fields.Nested(ConnectorSchema)

    @post_load
    def make_database(self, item, many, **kwargs) -> Database:
        return Database(**item)
