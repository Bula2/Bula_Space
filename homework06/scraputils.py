import requests
from bs4 import BeautifulSoup, Tag


def extract_news(parser):
    def extract_first_integer_from_tag(tag: Tag, separator: str) -> int:
        try:
            return 0 if tag is None else int(tag.text.split(separator)[0])
        except ValueError:
            return 0

    news_list = []

    links = parser.findAll("a", {"class": "storylink"})
    subtexts = parser.findAll("td", {"class": "subtext"})

    for i in range(len(links)):
        author = subtexts[i].find("a", {"class": "user"})
        comments = extract_first_integer_from_tag(subtexts[i].find_all("a")[-1], "\xa0")
        points = extract_first_integer_from_tag(subtexts[i].find("span", {"class": "score"}), " ")

        news_list.append(
            {
                "author": None if author is None else author.text,
                "comments": comments,
                "points": points,
                "title": links[i].text,
                "url": links[i]["href"],
            }
        )

    return news_list


def extract_next_page(parser):
    table = parser.body.center.table
    rows = []
    for row in table.findAll("tr"):
        rows.append(row)
    content = rows[3].findAll("tr")
    print(len(content))
    if len(content) < 92:
        return "newest"
    page = content[-1].findAll("td")[1]
    return page.find("a")["href"]


def get_news(url, n_pages=1):
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


# Checking:
test = get_news("https://news.ycombinator.com", 3)
print(test[5], "\n", test[10], "\n", test[15])
