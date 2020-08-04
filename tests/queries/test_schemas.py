from taliesin.connectors.v0.models import Connector
from taliesin.databases.v0.models import Database
from taliesin.queries.v0.models import Query
from taliesin.queries.v0.schemas import QuerySchema


def test_database_schema(db_session):
    connector = Connector(name="native", parameters={"path": ":memory:"})
    database = Database(name="main", description="Main database", connector=connector)
    db_session.add(database)
    db_session.commit()

    schema = QuerySchema()

    serialized = {
        "database_id": 1,
        "submitted_query": "SELECT 1 + 1",
    }

    deserialized = schema.load(serialized)
    assert deserialized.database_id == 1
    assert deserialized.submitted_query == "SELECT 1 + 1"
    assert deserialized.executed_query is None

    assert schema.dump(deserialized) == {
        "executed_query": None,
        "started": None,
        "ended": None,
        "database_id": 1,
        "results": None,
        "scheduled": None,
        "submitted_query": "SELECT 1 + 1",
        "id": None,
    }
