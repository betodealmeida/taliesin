from typing import Dict
from typing import Type

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import orm
from sqlalchemy import String
from sqlalchemy.orm import relationship
from taliesin.connectors.v0.base import BaseConnector
from taliesin.connectors.v0.helpers import get_connectors
from taliesin.connectors.v0.models import Connector
from taliesin.database import Base


class Database(Base):

    __tablename__ = "databases"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    description = Column(String(255), unique=True)
    connector = relationship("Connector", uselist=False, back_populates="database")

    def __init__(self, name: str, description: str, connector: Connector):
        self.name = name
        self.description = description
        self.connector = connector

        self.connection = self.get_connection()

    @orm.reconstructor
    def load_connection(self) -> None:
        self.connection = self.get_connection()

    def get_connection(self) -> BaseConnector:
        connectors: Dict[str, Type[BaseConnector]] = get_connectors()
        return connectors[self.connector.name](**self.connector.parameters)

    def __repr__(self) -> str:
        return f"<Database {self.name!r} ({self.description!r})>"
