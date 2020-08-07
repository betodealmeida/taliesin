from datetime import datetime
from datetime import timezone

import jwt
from freezegun import freeze_time
from taliesin.middleware import JWTAuth
from werkzeug.test import Client
from werkzeug.testapp import test_app as app
from werkzeug.wrappers import BaseResponse


def test_no_authorization():
    wrapped_app = JWTAuth(app, "secret")
    client = Client(wrapped_app, BaseResponse)

    resp = client.get("/")
    assert resp.status_code == 401


def test_authorization():
    wrapped_app = JWTAuth(app, "secret")
    client = Client(wrapped_app, BaseResponse)

    payload = {"allowed": {"/": ["GET"]}}
    auth_token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = client.get("/", headers=headers)
    assert resp.status_code == 200


def test_authorization_invalid_method():
    wrapped_app = JWTAuth(app, "secret")
    client = Client(wrapped_app, BaseResponse)

    payload = {"allowed": {"/": ["GET"]}}
    auth_token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = client.post("/", headers=headers)
    assert resp.status_code == 403


def test_authorization_invalid_path():
    wrapped_app = JWTAuth(app, "secret")
    client = Client(wrapped_app, BaseResponse)

    payload = {"allowed": {"/path": ["GET"]}}
    auth_token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = client.post("/", headers=headers)
    assert resp.status_code == 403


def test_authorization_expiration():
    wrapped_app = JWTAuth(app, "secret")
    client = Client(wrapped_app, BaseResponse)

    expiration = datetime(2020, 1, 1, 1, 0, 0, tzinfo=timezone.utc)
    payload = {"allowed": {"/": ["GET", "POST"]}, "exp": int(expiration.timestamp())}
    auth_token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")
    headers = {"Authorization": f"Bearer {auth_token}"}

    with freeze_time("2020-01-01T00:30:00Z"):
        resp = client.get("/", headers=headers)
    assert resp.status_code == 200

    with freeze_time("2020-01-01T01:30:00Z"):
        resp = client.get("/", headers=headers)
    assert resp.status_code == 401


def test_invalid_token():
    wrapped_app = JWTAuth(app, "secret")
    client = Client(wrapped_app, BaseResponse)

    headers = {"Authorization": f"Bearer BOGUS"}
    resp = client.post("/", headers=headers)
    assert resp.status_code == 401
