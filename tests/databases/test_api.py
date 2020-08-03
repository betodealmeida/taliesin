from taliesin.databases.v0.models import Connector
from taliesin.databases.v0.models import Database


def test_get_databases(mocker, db_session, client):
    # mocker.patch("taliesin.database.Base.query", db_session.query_property())

    connector = Connector(name="native", parameters={"path": ":memory:"})
    database = Database(
        name="native", description="Native database", connector=connector,
    )
    db_session.add(database)
    db_session.commit()

    response = client.get("/api/v0/databases")
    assert response.status_code == 200
    assert response.json == [
        {
            "connector": {
                "id": 1,
                "name": "native",
                "parameters": {"path": ":memory:"},
            },
            "id": 1,
            "description": "Native database",
            "name": "native",
        },
    ]


def test_post_databases(client):
    pass
