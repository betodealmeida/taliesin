from typing import Any
from typing import Dict

from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema
from taliesin.databases.v0.models import Database


SELF_PREFIX = "/databases/"


class DatabaseSchema(Schema):
    self = fields.Function(lambda obj: f"{SELF_PREFIX}{obj.alias}", required=True)
    alias = fields.Str(required=True)
    name = fields.Str(required=True)

    @post_load
    def make_database(self, data: Dict[str, Any]) -> Database:
        id_ = data.pop("self")[len(SELF_PREFIX) :]
        return Database(id=id_, **data)
