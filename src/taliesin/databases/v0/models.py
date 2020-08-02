from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from taliesin.database import Base


class Database(Base):

    __tablename__ = "databases"
    id = Column(Integer, primary_key=True)
    alias = Column(String(50), unique=True)
    name = Column(String(50), unique=True)

    def __init__(self, alias: str, name: str):
        self.alias = alias
        self.name = name

    def __repr__(self) -> str:
        return "<Database %r (%r)>" % (self.alias, self.name)
