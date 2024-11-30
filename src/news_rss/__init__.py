import collections
import csv
import datetime
import pathlib
import tempfile
import tomllib
import uuid

from chdb import session
import spacy

from news_rss import google


def load_config(path: pathlib.Path):
    return tomllib.loads(path.read_text())


def get_session(config):
    return session.Session(config["store"]["clickhouse"]["path"])


def scrape(config):
    news = scrape_google_news(config["sources"]["google_news"])

    chdb = get_session(config)
    chdb.query("""
    create database if not exists news;
    create table if not exists news.google_news_v1 (
      google_news_url String,
      section_title String,
      section_language String,
      news_item_id UUID,
      title String,
      source String,
      url String,
      when Datetime
    ) engine = MergeTree
    order by tuple();
    """)

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        data_path = tempdir / "data.csv"
        with open(data_path, "w", newline="") as f:
            csv.writer(f).writerows(news)

        chdb.query(f"""
        insert into news.google_news_v1 select * from file("{data_path}", CSV)
        """)


def scrape_google_news(google_news_urls):
    for google_news_url in google_news_urls:
        ts = datetime.datetime.now()
        rss = google.news_url_to_rss_url(google_news_url)
        rss = google.process_feed_url(rss)
        for news_item in rss.news_items:
            id = uuid.uuid4()
            for piece in news_item:
                yield (
                    google_news_url,
                    rss.title,
                    rss.language,
                    id,
                    piece.title,
                    piece.source,
                    piece.google_news_url,
                    int(ts.timestamp()),
                )


def download_models(config):
    chdb = get_session(config)
    df = chdb.query(
        "select distinct section_language from news.google_news_v1", "dataframe"
    )
    for language in df["section_language"]:
        model = config["spacy"]["models"][language]
        spacy.cli.download(model)


def shown_ner(config):
    ner = collections.Counter()
    labels = set()
    chdb = get_session(config)
    df = chdb.query(
        "select distinct section_language, title from news.google_news_v1", "dataframe"
    )
    models = {}
    for _, row in df.iterrows():
        language = row["section_language"]
        if not language in models:
            models[language] = spacy.load(config["spacy"]["models"][language])
        doc = models[language](row["title"])
        labels = labels.union([e.label_ for e in doc.ents])
        ner.update([e.text for e in doc.ents])
    print(ner.most_common(100))
