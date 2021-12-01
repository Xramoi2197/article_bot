import sqlalchemy
from sqlalchemy.orm import sessionmaker

from ..additional.func import get_url_date


from .models import User, Article, ArticleTag, Tag


def create_engine(conn_str: str):
    return sqlalchemy.create_engine(conn_str)


def make_session(db_engine: sqlalchemy.engine.Engine):
    Session = sessionmaker(bind=db_engine)
    return Session()


def add_article(db_engine: sqlalchemy.engine.Engine, tg_user_id: int, url_str: str):
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
    url_data = get_url_date(url_str=url_str)
    if url_data != None:
        new_article = Article(title=url_data[0], url=url_str, user_id=db_user_id)
        session.add(new_article)
        session.commit()
        return new_article.title
    return None


def get_articles_page(
    db_engine: sqlalchemy.engine.Engine, tg_user_id: int, page_num: int
):
    if page_num < 1:
        return []
    session = make_session(db_engine=db_engine)
    result = []
    articles_per_page = 5
    articles = (
        session.query(User)
        .filter(User.tg_user_id == tg_user_id)
        .one()
        .articles.order_by(Article.create_date.asc())
        .offset((page_num - 1) * articles_per_page)
        .limit(articles_per_page)
    )
    if not articles:
        return []
    for article in articles:
        result.append((article.title, article.url))
    return result
