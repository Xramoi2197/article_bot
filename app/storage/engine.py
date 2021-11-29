import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import user


from .models import Base, User, Article, ArticleTag, Tag


def create_engine(conn_str: str):
    return sqlalchemy.create_engine(conn_str)


def make_session(db_engine: sqlalchemy.engine.Engine):
    Session = sessionmaker(bind=db_engine)
    return Session()


def add_article(db_conn_str: str, tg_user_id: int, url: str):
    db_engine = create_engine(db_conn_str)
    session = make_session(db_engine=db_engine)
    db_user_id = None
    query_results = session.query(User).filter(User.tg_user_id == tg_user_id)
    if query_results.count() != 1:
        new_user = User(tg_user_id=tg_user_id)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        db_user_id = new_user.id
    else:
        db_user_id = query_results.first().id
    return db_user_id
