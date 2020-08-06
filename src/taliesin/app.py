from typing import Any
from typing import Dict

from flask import Flask
from taliesin.connectors.v0 import api as connectors_v0
from taliesin.database import init_app
from taliesin.databases.v0 import api as databases_v0


def create_app(test_config: Dict[str, Any] = None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("settings.py", silent=True)  # pragma: no cover
    else:
        app.config.from_mapping(test_config)

    init_app(app)

    app.config["JSON_SORT_KEYS"] = False

    app.register_blueprint(databases_v0.blueprint)
    app.register_blueprint(connectors_v0.blueprint)

    return app
