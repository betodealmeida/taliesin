from flask import Flask
from taliesin.connectors.v0 import api as connectors_v0
from taliesin.database import db_session
from taliesin.database import init_db
from taliesin.databases.v0 import api as databases_v0

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.register_blueprint(databases_v0.blueprint)
app.register_blueprint(connectors_v0.blueprint)

init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
