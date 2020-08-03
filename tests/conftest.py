# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from taliesin.app import app
from taliesin.database import Base


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite://")


@pytest.yield_fixture(scope="session")
def tables(engine):
    import taliesin.connectors.v0.models
    import taliesin.databases.v0.models
    import taliesin.queries.v0.models

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.yield_fixture
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine),
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.yield_fixture
def client():
    with app.test_client() as test_client:
        yield test_client
