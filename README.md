# news-rss

## Google

```
>>> from news_rss import google
>>> # obtain the RSS feed for a Google News URL
>>> google.news_url_to_rss_url("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen")
'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
>>> # parse the feed
>>> google_news_feed = google.process_feed_url('https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen')
>>> google_news_feed.title
'Business - Latest - Google News'
>>> google_news_feed.language
'en-US'
>>> news_item = list(google_news_feed.news_items)[0]
>>> for link in news_item:
...     print(link.title, link.source, link.google_news_url[0:40])
...
Germany in economic doldrums amid Trump tariff war, China competition Fox Business https://news.google.com/rss/articles/CBM
German economy grows slower than expected in third quarter DW (English) https://news.google.com/rss/articles/CBM
How Germany Can Make Peace With Trump on Trade Bloomberg https://news.google.com/rss/articles/CBM
Why Germany’s Economy, Once a Leader in Europe, Is Now in Crisis The New York Times https://news.google.com/rss/articles/CBM
Downgraded economic growth underscores challenges facing Germany Semafor https://news.google.com/rss/articles/CBM
```
