from sqlalchemy import Integer, String, DateTime, Column, ForeignKey
from sqlalchemy.sql.schema import CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime


MAX_ARTICLE_TITLE_LENGHT = 250
MAX_ARTICLE_URL_LENGHT = 300
MAX_TAG_NAME_LENGHT = 50
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    tg_user_id = Column(Integer(), nullable=False, unique=True)
    articles = relationship("Article", backref="users", lazy='dynamic', passive_deletes=True)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer(), primary_key=True)
    tag_name = Column(String(MAX_TAG_NAME_LENGHT), nullable=False)
    articles = relationship("Article", secondary="article_tags", back_populates="tags")


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer(), primary_key=True)
    title = Column(String(MAX_ARTICLE_TITLE_LENGHT), nullable=False)
    url = Column(String(MAX_ARTICLE_URL_LENGHT), nullable=False, unique=True)
    create_date = Column(DateTime(), default=datetime.now, nullable=False)
    mark = Column(Integer(), default=0)
    last_show_date = Column(DateTime(), nullable=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    tags = relationship(Tag, secondary="article_tags", back_populates="articles")
    __table_args__ = (CheckConstraint("-1 < mark and mark < 11", name="mark_check"),)


class ArticleTag(Base):
    __tablename__ = "article_tags"
    id = Column(Integer, primary_key=True)
    article_id = Column(ForeignKey("articles.id", ondelete="CASCADE"))
    tag_id = Column(ForeignKey("tags.id", ondelete="CASCADE"))
