# type: ignore
import string

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@tp.no_type_check
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@tp.no_type_check
@route("/add_label/")
def add_label():
    query = request.query.decode()
    identifier = int(query["id"])
    label = query["label"]
    s = session()
    update_label(s, identifier, label)
    s.commit()
    redirect("/news")


def update_label(session, news_id, label) -> None:
    session.query(News.id).filter(News.id == news_id).update({News.label: label})


def has(ses: Session, author: str, title: str) -> bool:
    return (
        len(ses.query(News.author).filter_by(author=author).all()) == 0
        or len(ses.query(News.title).filter_by(title=title).all()) == 0
    )


@tp.no_type_check
@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/", 3)
    s = session()
    update_news_db(s, news)
    s.commit()
    redirect("/news")


def update_news_db(session: Session, news: tp.List[tp.Dict[str, tp.Union[str, int]]]) -> None:
    for n in news:
        if has(session, n["author"], n["title"]):
            session.add(
                News(
                    title=n["title"],
                    author=n["author"],
                    url=n["url"],
                    points=n["points"],
                    comments=n["comments"],
                )
            )


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


@tp.no_type_check
@route("/classify")
def classify_news():
    s = session()
    model = NaiveBayesClassifier()
    train_set = get_train_set(s, News)
    model.fit(
        [clean(news.title).lower() for news in train_set],
        [news.label for news in train_set],
    )
    test = get_test_set(s, News)
    return template(
        "news_template",
        rows=sorted(test, key=lambda news: get_weight(model.predict(clean(news.title).lower()))),
    )


def get_train_set(session: Session, news_obj: str) -> str:
    return session.query(News).filter(news_obj.label != None).all()


def get_test_set(session: Session, news_obj: str) -> str:
    return session.query(News).filter(news_obj.label == None).all()


def get_weight(label: str) -> str:
    if label == "never":
        return 2
    elif label == "maybe":
        return 1
    elif label == "good":
        return 0
    else:
        return "Invalid label" + label


if __name__ == "__main__":
    run(host="localhost", port=8080)
