import feedparser
from pprint import pprint
from tools.webscraper import scrape_feed_content


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


# Fetch rss data and store it into databse.
def fetch_rss_feeds(rss_links: list[str]) -> list[dict]:
    
    all_feeds = []
    
    # get title, category, publish date and link of all the passages from rss feed.
    for link in rss_links:
        feeds = load_rss_feed(link=link)
        print(f"Total feeds per rss - {link}: {len(feeds)}")
        
        # scrape all the passage contents.
        for feed in feeds:
            content = scrape_feed_content(news_url=feed["Feed_URL"])
            feed["Content"]=content
            all_feeds.append(feed)
            
    return all_feeds