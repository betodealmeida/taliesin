from taliesin.databases.v0.models import Connector
from taliesin.databases.v0.models import Database


def test_database(db_session):
    connector = Connector(name="native", parameters={"path": ":memory:"})
    database = Database(
        name="native", description="Native database", connector=connector,
    )
    db_session.add(database)
    db_session.commit()

    assert db_session.query(Database).all() == [database]
    assert db_session.query(Connector).all() == [connector]

    database = db_session.query(Database).first()
    assert str(database) == "<Database 'native' ('Native database')>"
    assert database.connection == ""
