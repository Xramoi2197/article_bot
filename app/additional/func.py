import validators
import requests
from bs4 import BeautifulSoup

from ..storage.models import MAX_ARTICLE_TITLE_LENGHT

OK = 200


def is_url(url_string: str) -> bool:
    result = validators.url(url_string)
    if isinstance(result, validators.ValidationFailure):
        return False
    return result


def get_url_date(url_str: str):
    response = requests.get(url_str)
    if response.status_code != OK:
        return None
    title = url_str[:MAX_ARTICLE_TITLE_LENGHT]
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all("title")
    if len(titles) > 0:
        title = titles[0].get_text()[:MAX_ARTICLE_TITLE_LENGHT]
    return (title,)
