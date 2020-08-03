from typing import Dict
from typing import Type

from pkg_resources import iter_entry_points
from taliesin.connectors.v0.base import BaseConnector


def get_connectors() -> Dict[str, Type[BaseConnector]]:
    return {
        entry_point.name: entry_point.load()
        for entry_point in iter_entry_points("taliesin.connector")
    }
