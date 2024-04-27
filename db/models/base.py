from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"sqlite_autoincrement": True}
