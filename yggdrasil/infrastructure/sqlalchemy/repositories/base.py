from abc import ABC

from yggdrasil.infrastructure.sqlalchemy import SQLAlchemy


class BaseSARepository(ABC):
    def __init__(self, sa: SQLAlchemy) -> None:
        self.sa = sa
