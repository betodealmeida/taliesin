import os
from typing import Any
from typing import Callable
from typing import Dict

from flask import Flask
from taliesin.connectors.v0 import api as connectors_v0
from taliesin.database import init_app
from taliesin.databases.v0 import api as databases_v0
from taliesin.middleware import JWTAuth


def create_app(test_config: Dict[str, Any] = None):
    app = Flask(__name__)
    app.config.from_mapping({"JSON_SORT_KEYS": False})
    if test_config is not None:
        app.config.from_mapping(test_config)
    else:  # pragma: no cover
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]

    # init database engine and session
    init_app(app)

    app.register_blueprint(databases_v0.blueprint)
    app.register_blueprint(connectors_v0.blueprint)

    if os.environ.get("SECRET"):
        app.wsgi_app = JWTAuth(app.wsgi_app, os.environ["SECRET"])  # type: ignore

    return app
