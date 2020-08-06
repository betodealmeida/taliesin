import os
from typing import Any

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


Base = declarative_base()  # type: Any


def init_app(app: Flask):
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], convert_unicode=True)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine),
    )

    app.db_session = db_session
    Base.query = db_session.query_property()

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import taliesin.connectors.v0.models
    import taliesin.databases.v0.models
    import taliesin.queries.v0.models

    Base.metadata.create_all(bind=engine)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
