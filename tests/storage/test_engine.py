import unittest
import sys
sys.path.append("../..")
from app.storage.engine import create_engine, make_session, add_article
from app.storage.models import Base, Article, ArticleTag, Tag, User


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.conn_str = "sqlite:///:memory:"
        self.engine = create_engine(self.conn_str)
        self.session = make_session(self.engine)
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_add_new_article(self):
        tg_user_id = 123456
        url_str = "https://google.com"
        result = add_article(self.engine, tg_user_id, url_str)
        title = self.session.query(Article).filter(Article.title == result).first().title
        self.assertEqual(result, title)

if __name__ == "__main__":
  unittest.main()