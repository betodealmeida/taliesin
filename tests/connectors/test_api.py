import json

from freezegun import freeze_time
from taliesin.connectors.v0.base import BaseConnector
from taliesin.connectors.v0.models import Connector
from taliesin.databases.v0.models import Database


class DummyConnector(BaseConnector):

    name = "dummy"
    parameters = {
        "name": name,
        "title": "Dummy connector",
    }


def test_get_connectors(mocker, client):
    mocker.patch(
        "taliesin.connectors.v0.api.load_connectors",
        return_value={"dummy": DummyConnector},
    )

    response = client.get("/api/v0/connectors")
    assert response.status_code == 200
    assert response.json == [
        {"name": "dummy", "parameters": {"name": "dummy", "title": "Dummy connector"}},
    ]
