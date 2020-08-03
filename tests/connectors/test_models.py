from taliesin.connectors.v0.models import Connector


def test_connector(db_session):
    connector = Connector(name="native", parameters={"path": ":memory:"})
    db_session.add(connector)
    db_session.commit()

    assert db_session.query(Connector).all() == [connector]
