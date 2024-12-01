# news-rss

Download and parse Google News RSS feeds following the configuration in `news.toml`:

```
$ news-rss news.toml scrape
```

Download the spaCy models corresponding to the languages in the configuration:

```
$ news-rss news.toml download_models
```

Perform "named entity" recognition of scraped news and display the most frequent entities in the scraped data:

```
$ news-rss news.toml show_ner
[('Black Friday', 160), ('Amazon', 55),  ...
```

## Hacking

This project uses [uv](https://docs.astral.sh/uv/).

Prefix the previous commands with `uv run` to have uv set up a development environment and run the commands.
