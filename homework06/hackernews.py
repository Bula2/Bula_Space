from bottle import (
    route, run, template, request, redirect
)
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label is None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query["label"]
    id = request.query["id"]
    print(label, id)
    s = session()
    page = s.query(News).get(id)
    page.label = label
    s.add(page)
    s.commit()
    print(page.title)
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    pages = get_news("https://news.ycombinator.com/newest", 1)
    for i in range(len(pages)):
        news = News(
            title=pages[i]["title"],
            author=pages[i]["author"],
            comments=pages[i]["comments"],
            points=pages[i]["points"],
            url=pages[i]["url"],
        )
        if s.query(News).filter(News.title == news.title and News.author == news.author).count() == 0:
            s.add(news)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    ...


if __name__ == "__main__":
    run(host="localhost", port=8080)
