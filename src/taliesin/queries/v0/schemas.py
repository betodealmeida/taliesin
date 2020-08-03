from typing import Any
from typing import Dict

from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema
from taliesin.connectors.v0.schemas import ConnectorSchema
from taliesin.queries.v0.models import Query


class QuerySchema(Schema):
    id = fields.Integer()
    database_id = fields.Integer(required=True)
    submitted_query = fields.Str(required=True)
    executed_query = fields.Str(allow_none=True)
    scheduled = fields.DateTime(format="iso", allow_none=True)
    started = fields.DateTime(format="iso", allow_none=True)
    ended = fields.DateTime(format="iso", allow_none=True)
    results = fields.List(
        fields.Dict(keys=fields.Str(), values=fields.Raw()), allow_none=True,
    )

    @post_load
    def make_query(self, item, many, **kwargs) -> Query:
        return Query(**item)
