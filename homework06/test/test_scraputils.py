# type: ignore
import scraputils
from bs4 import BeautifulSoup
import requests


def test_extract_next_page():
    url = "https://news.ycombinator.com/"
    for i in range(2, 5):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        next_url = scraputils.extract_next_page(soup)
        assert next_url == "news?p=" + str(i)
        url = "https://news.ycombinator.com/" + next_url


def test_extract_news():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    current_news = scraputils.extract_news(soup)
    news_keys = {"author", "url", "points", "title", "comments"}
    assert set(current_news[0].keys()) == news_keys


def test_get_news():
    news = []
    url = "https://news.ycombinator.com/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    current_news = scraputils.extract_news(soup)
    next_url = scraputils.extract_next_page(soup)
    url = "https://news.ycombinator.com/" + next_url
    news.extend(current_news)

    assert scraputils.get_news("https://news.ycombinator.com/") == news
