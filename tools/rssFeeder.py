import feedparser
from pprint import pprint

# load RSS feeds from RSS link.
def load_rss_feed(link: str) -> list[dict]:
    
    # parse the RSS feed.
    feed = feedparser.parse(link)
    rss_feeds = []

    for item in feed.entries:
        feed_dict = {
            "Category": feed.feed.title,
            "Title": item.title,
            "Publish_Date": item.published,
            "Feed_URL": item.link,
            "Summary": item.summary
            }
        rss_feeds.append(feed_dict)

    return rss_feeds


