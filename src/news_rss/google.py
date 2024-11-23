import dataclasses
from urllib import parse

import bs4
import httpx
import rss_parser


def news_url_to_rss_url(url):
    url = parse.urlparse(url)
    assert url.netloc == "news.google.com"
    url = url._replace(path="/rss" + url.path).geturl()
    rss_parser.RSSParser.parse(httpx.get(url).text)
    return url


def process_feed_url(url):
    feed = rss_parser.RSSParser.parse(httpx.get(url).text)
    return GoogleNewsFeed(
        title=feed.channel.content.title.content,
        language=feed.channel.content.language.content,
        news_items=frozenset(_feed_items_to_set_of_news_items(feed.channel.items)),
    )


def _feed_items_to_set_of_news_items(items):
    for item in items:
        html = item.description.content
        html = bs4.BeautifulSoup(html, features="html.parser")
        yield frozenset(map(_news_item_from, html.find_all("li")))


@dataclasses.dataclass(eq=True, frozen=True)
class NewsItem:
    google_news_url: str
    title: str
    source: str


@dataclasses.dataclass
class GoogleNewsFeed:
    title: str
    language: str
    news_items: frozenset[frozenset[NewsItem]]


def _news_item_from(li):
    return NewsItem(
        google_news_url=li.find("a").get("href"),
        title=li.find("a").text,
        source=li.find("font").text,
    )
