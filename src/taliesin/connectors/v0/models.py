from typing import Any
from typing import Dict

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import relationship
from taliesin.database import Base


class Connector(Base):

    __tablename__ = "connectors"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    parameters = Column(JSON)

    database_id = Column(Integer, ForeignKey("databases.id"))
    database = relationship("Database", back_populates="connector")

    def __init__(self, name: str, parameters: Dict[str, Any]):
        self.name = name
        self.parameters = parameters

    def __repr__(self) -> str:
        return "<Connector %r>" % (self.name)
