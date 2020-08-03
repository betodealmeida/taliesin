from taliesin.connectors.v0.models import Connector
from taliesin.connectors.v0.schemas import ConnectorSchema


def test_connector_schema():
    schema = ConnectorSchema()

    serialized = {
        "name": "native",
        "parameters": {"path": ":memory:"},
    }

    deserialized = schema.load(serialized)
    assert deserialized.name == "native"
    assert deserialized.parameters == {"path": ":memory:"}

    deserialized.id = 1
    assert schema.dump(deserialized) == {
        "id": 1,
        "name": "native",
        "parameters": {"path": ":memory:"},
    }
