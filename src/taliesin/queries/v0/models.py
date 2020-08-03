from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import orm
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from taliesin.database import Base


class Query(Base):

    __tablename__ = "queries"
    id = Column(Integer, primary_key=True)
    database_id = Column(Integer, ForeignKey("databases.id"))
    database = relationship("Database")

    submitted_query = Column(Text)
    executed_query = Column(Text)

    scheduled = Column(DateTime(timezone=True))
    started = Column(DateTime(timezone=True))
    ended = Column(DateTime(timezone=True))

    # state =
    # progress =
    # results_key =

    def __init__(
        self,
        database_id: int,
        submitted_query: str,
        executed_query: Optional[str] = None,
        scheduled: Optional[datetime] = None,
        started: Optional[datetime] = None,
        ended: Optional[datetime] = None,
        results: Optional[List[Dict[str, Any]]] = None,
    ):
        self.database_id = database_id
        self.submitted_query = submitted_query
        self.executed_query = executed_query
        self.scheduled = scheduled
        self.started = started
        self.ended = ended
        self.results = results

    @orm.reconstructor
    def load_results(self) -> None:
        # TODO: load from results backend
        self.results = None

    def __repr__(self) -> str:
        return f"<Query {self.id!r} ({self.submitted_query!r}>"
