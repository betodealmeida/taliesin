from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:////tmp/test.db", convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine),
)
Base = declarative_base()  # type: Any
Base.query = db_session.query_property()


def init_db() -> None:
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import taliesin.connectors.v0.models
    import taliesin.databases.v0.models

    Base.metadata.create_all(bind=engine)
