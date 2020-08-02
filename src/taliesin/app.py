from flask import Flask
from taliesin.database import init_db
from taliesin.databases.v0 import api as databases_v0

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.register_blueprint(databases_v0.blueprint)

init_db()
