import json

from freezegun import freeze_time
from taliesin.connectors.v0.models import Connector
from taliesin.databases.v0.models import Database


def test_get_databases(client):
    db_session = client.application.db_session
    connector = Connector(name="native", parameters={"path": ":memory:"})
    database = Database(name="main", description="Main database", connector=connector)
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
            "description": "Main database",
            "name": "main",
        },
    ]


def test_post_databases(client):
    payload = {
        "name": "main",
        "description": "Main database",
        "connector": {"name": "native", "parameters": {"path": ":memory:"}},
    }
    response = client.post(
        "/api/v0/databases", data=json.dumps(payload), content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json == {
        "name": "main",
        "description": "Main database",
        "id": 1,
        "connector": {"name": "native", "parameters": {"path": ":memory:"}, "id": 1},
    }

    databases = Database.query.all()
    assert len(databases) == 1
    assert databases[0].id == 1


def test_post_queries(client):
    db_session = client.application.db_session
    connector = Connector(name="native", parameters={"path": ":memory:"})
    database = Database(name="main", description="Main database", connector=connector)
    db_session.add(database)
    db_session.commit()

    payload = {
        "submitted_query": "SELECT 1 + 1",
    }
    with freeze_time("2020-01-01T00:00:00Z"):
        response = client.post(
            "/api/v0/databases/main/queries",
            data=json.dumps(payload),
            content_type="application/json",
        )
    assert response.status_code == 201
    assert response.json == {
        "submitted_query": "SELECT 1 + 1",
        "started": "2020-01-01T00:00:00",
        "results": [{"1 + 1": 2}],
        "id": 1,
        "scheduled": "2020-01-01T00:00:00",
        "executed_query": "SELECT 1 + 1",
        "ended": "2020-01-01T00:00:00",
        "database_id": 1,
    }
