from datetime import datetime
from datetime import timezone

from freezegun import freeze_time
from taliesin.connectors.v0.models import Connector
from taliesin.connectors.v0.native import NativeConnector
from taliesin.databases.v0.models import Database
from taliesin.queries.v0.models import Query


def test_submit_query(db_session):
    connector = Connector(name="native", parameters={"path": ":memory:"})
    database = Database(name="main", description="Main database", connector=connector)
    db_session.add(database)
    db_session.commit()

    connector = NativeConnector(":memory:")
    query = Query(database_id=1, submitted_query="SELECT 1 + 1")

    with freeze_time("2020-01-01T00:00:00Z"):
        query = connector.submit_query(query)

    assert query.scheduled == datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert query.started == datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert query.ended == datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc)

    assert query.executed_query == "SELECT 1 + 1"
    assert query.results == [{"1 + 1": 2}]


def test_get_query(db_session):
    connector = Connector(name="native", parameters={"path": ":memory:"})
    database = Database(name="main", description="Main database", connector=connector)
    db_session.add(database)
    db_session.commit()

    query = Query(database_id=1, submitted_query="SELECT 1 + 1")
    db_session.add(query)
    db_session.commit()

    connector = NativeConnector(":memory:")
    query = connector.get_query(1)
    assert query.submitted_query == "SELECT 1 + 1"
