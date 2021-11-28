import sqlalchemy
from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker


from .models import Base, User, Article, ArticleTag, Tag


def create_engine(conn_str: str):
    return sqlalchemy.create_engine(conn_str)


def make_session(db_engine: sqlalchemy.engine.Engine):
    Session = sessionmaker(bind=db_engine)
    return Session()

