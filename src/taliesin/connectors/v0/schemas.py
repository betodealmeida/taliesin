from typing import Any
from typing import Dict

from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema
from taliesin.connectors.v0.models import Connector


class ConnectorSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True)
    parameters = fields.Mapping()

    @post_load
    def make_connector(self, item, many, **kwargs) -> Connector:
        return Connector(**item)
