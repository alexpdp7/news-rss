import argparse
import pathlib

import news_rss


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=pathlib.Path)

    subparsers = parser.add_subparsers(required=True)

    subparser = subparsers.add_parser("scrape")

    def scrape(_args):
        news_rss.scrape(config)

    subparser.set_defaults(func=scrape)

    args = parser.parse_args()

    config = news_rss.load_config(args.config)

    args.func(args)