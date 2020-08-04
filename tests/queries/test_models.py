from taliesin.connectors.v0.models import Connector
from taliesin.databases.v0.models import Database
from taliesin.queries.v0.models import Query


def test_query(db_session):
    connector = Connector(name="native", parameters={"path": ":memory:"})
    database = Database(name="main", description="Main database", connector=connector)
    db_session.add(database)
    db_session.commit()

    query = Query(database_id=1, submitted_query="SELECT 1 + 1")
    db_session.add(query)
    db_session.commit()

    assert db_session.query(Query).all() == [query]
    assert db_session.query(Connector).all() == [connector]

    query = db_session.query(Query).first()
    assert str(query) == "<Query 1 ('SELECT 1 + 1')>"
