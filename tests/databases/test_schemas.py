from taliesin.databases.v0.models import Database
from taliesin.databases.v0.schemas import DatabaseSchema


def test_database_schema():
    schema = DatabaseSchema()

    serialized = {
        "name": "native",
        "description": "Native database",
        "connector": {"name": "native", "parameters": {"path": ":memory:"}},
    }

    deserialized = schema.load(serialized)
    assert deserialized.name == "native"
    assert deserialized.description == "Native database"
    assert deserialized.connector.name == "native"
    assert deserialized.connector.parameters == {"path": ":memory:"}

    deserialized.id = 1
    deserialized.connector.id = 1
    assert schema.dump(deserialized) == {
        "id": 1,
        "name": "native",
        "description": "Native database",
        "connector": {"id": 1, "name": "native", "parameters": {"path": ":memory:"}},
    }
